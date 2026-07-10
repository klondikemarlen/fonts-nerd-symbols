# Debian-first package submission

Use this path when you want `fonts-nerd-symbols` to become an official Debian package first, then flow into Ubuntu by normal sync.

Use `debian/latest` as the long-lived Debian packaging branch. Keep PPA/GitHub release work on `main` so Ubuntu series changelog targets such as `resolute` do not accidentally switch to `unstable`.

## Flow

1. File an ITP bug for `fonts-nerd-symbols`.
2. Update `debian/changelog` to close it: `Closes: #NNNNNN`.
3. Set the changelog distribution to `unstable` on the Debian packaging branch.
4. Build a signed source package with `debuild -S -sa` for a new upstream orig tarball, or `debuild -S -sd` for later Debian revisions of the same upstream version.
5. Run `lintian` on the source `.changes` and `.dsc`.
6. Sign the source artifacts with the registered OpenPGP key.
7. Upload to mentors.debian.net.
8. File an RFS bug against `sponsorship-requests` by sending the mentors RFS template to `submit@bugs.debian.org`.
9. Pass Debian NEW review.
10. Ubuntu can later sync the package from Debian.

## File the ITP

Install and configure `reportbug`:

```bash
sudo apt install reportbug
reportbug --configure
```

For Ubuntu hosts, make sure `reportbug` targets Debian, not Ubuntu:

```bash
reportbug -B debian wnpp
```

If `reportbug` starts paging through thousands of existing WNPP bugs, quit and rerun without the duplicate-query browser:

```bash
reportbug -B debian --no-query-bts wnpp
```

Choose `ITP - Intent To Package`.

Suggested metadata:

```text
Package: fonts-nerd-symbols
Short description: Nerd Fonts symbols fallback for fontconfig
License: DFSG-free rebuilt Symbols Nerd Font, excluding Font Logos
Upstream: https://github.com/ryanoasis/nerd-fonts
Packaging: https://salsa.debian.org/klondikemarlen/fonts-nerd-symbols/-/tree/debian/latest
```

Suggested long description:

```text
Installs Symbols Nerd Font and fontconfig aliases so existing terminal fonts
such as Ubuntu Sans Mono can render Nerd Font icon glyphs without switching
the whole terminal font.
```

Mention these specifics in the bug or sponsor notes:

- this is a fonts package, not an application;
- the package rebuilds the Nerd Fonts Symbols Only assets from upstream source inputs;
- Font Logos is excluded because upstream marks it unlicensed and Debian notes flag logo glyphs as likely non-distributable;
- the completed [DFSG/provenance audit](dfsg-audit.md) records every included glyph source, license, preferred form for modification, and the Font Logos exclusion;
- normal text continues to render with the user's selected monospace font;
- `Symbols Nerd Font` is only a fallback for missing icon/private-use glyphs;
- the intended install paths are under `/usr/share/fonts/truetype/nerd-fonts-symbols/`, `/usr/share/fontconfig/conf.avail/`, and `/etc/fonts/conf.d/`.

## Changelog for Debian

Current Debian tracker state:

```text
ITP: #1141696
RFS: #1141699
Current mentors upload: pending refreshed 3.4.0+dfsg-2 upload
```

For a future first upload of a new package, after the ITP exists, update `debian/changelog` on the Debian branch:

```text
fonts-nerd-symbols (NEXT_VERSION) unstable; urgency=medium

  * Initial release. (Closes: #NNNNNN)

 -- Marlen Brunner <klondikemarlen+debian@gmail.com>  DATE
```

Use the public Debian packaging email you used for the ITP. Do not change the PPA branch from `resolute` to `unstable`; keep Debian submission work on `debian/latest`.

## Build source for review

Build Debian uploads in Debian, not Ubuntu. Ubuntu's `lintian` can reject `Distribution: unstable`, and Ubuntu-built source metadata can include Ubuntu-specific build context.

A disposable Debian container is enough for this package:

```bash
docker run --rm -v "$PWD:/work" -w /work debian:unstable sh -lc '
  set -eu
  export DEBIAN_FRONTEND=noninteractive
  apt-get update >/dev/null
  apt-get install -y --no-install-recommends \
    ca-certificates git xz-utils dpkg-dev devscripts debhelper lintian build-essential fontforge python3-fontforge fontconfig >/dev/null
  rm -rf build
  UPSTREAM_VERSION="$(dpkg-parsechangelog -S Version | sed "s/-[^-]*$//")"
  SOURCE_VERSION="$(dpkg-parsechangelog -S Version)"
  ./debian/scripts/prepare-upstream "$UPSTREAM_VERSION"
  cd "build/fonts-nerd-symbols-$UPSTREAM_VERSION"
  debuild -S -sa -us -uc
  lintian --profile debian "../fonts-nerd-symbols_${SOURCE_VERSION}_source.changes" "../fonts-nerd-symbols_${SOURCE_VERSION}.dsc"
'
```

Use `-sa` for the first Debian upload of a new upstream orig tarball. Use `-sd` only for later Debian revisions of the same upstream version after the orig tarball is already in the target archive.

Sign the regenerated source upload with the registered key:

```bash
debsign -kFULL_FINGERPRINT build/fonts-nerd-symbols_${SOURCE_VERSION}_source.changes
```

The `.dsc`, `.buildinfo`, and `_source.changes` files should begin with a PGP signed message header after signing.

## Upload to mentors

Register the same public OpenPGP key in your mentors.debian.net account. Export only the public key:

```bash
gpg --export --export-options export-minimal --armor FULL_FINGERPRINT
```

Do not export or upload secret keys.

Upload the signed source package:

```bash
dput mentors build/fonts-nerd-symbols_${SOURCE_VERSION}_source.changes
```

If the `mentors` dput profile is missing, use the mentors.debian.net web upload or add the mentors upload profile from their maintainer instructions.

After mentors accepts the upload, it sends the public package page, `.dsc` URL, and an RFS helper URL. Use those links in the sponsorship request instead of guessing paths.

## Submit for sponsorship

After mentors accepts the upload and shows a package page, file an RFS bug against `sponsorship-requests` by sending the mentors RFS template to `submit@bugs.debian.org`.

For the initial Debian submission of this package:

```text
ITP: #1141696
RFS: #1141699
Mentors upload: <version shown by mentors.debian.net after upload>
DSC: <https://mentors.debian.net/debian/pool/main/f/fonts-nerd-symbols/fonts-nerd-symbols_VERSION.dsc>
Debian packaging branch: https://salsa.debian.org/klondikemarlen/fonts-nerd-symbols/-/tree/debian/latest
```

Typical RFS subject:

```text
RFS: fonts-nerd-symbols/3.4.0+dfsg-2 [ITP] -- Nerd Fonts symbols fallback for fontconfig
```

Include the ITP bug number, mentors package URL, source package URL, lintian result, a short note that this is a fonts/fontconfig fallback package, and the completed DFSG/provenance audit.

Sponsor review will focus on licensing, source/orig tarball construction, preferred form for modification for bundled glyph sources, Debian font paths, fontconfig behavior, lintian output, and whether generated/binary font assets are handled according to Debian policy.
