# Debian-first package submission

Use this path when you want `fonts-nerd-symbols` to become an official Debian package first, then flow into Ubuntu by normal sync. Keep this separate from the PPA branch so Ubuntu-series uploads can keep targeting `resolute`.

```bash
git switch -c debian-submission
```

## Flow

1. File an ITP bug for `fonts-nerd-symbols`.
2. Update `debian/changelog` to close it: `Closes: #NNNNNN`.
3. Set the changelog distribution to `unstable` on the Debian submission branch.
4. Build a source package in a Debian environment.
5. Run Debian `lintian` on the source `.changes` and `.dsc`.
6. Sign the source artifacts with the registered OpenPGP key.
7. Upload the source package to mentors.debian.net.
8. File an RFS bug and find a Debian sponsor.
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
License: MIT
Upstream: https://github.com/ryanoasis/nerd-fonts
Packaging: https://github.com/klondikemarlen/fonts-nerd-symbols
```

Suggested long description:

```text
Installs Symbols Nerd Font and fontconfig aliases so existing terminal fonts
such as Ubuntu Sans Mono can render Nerd Font icon glyphs without switching
the whole terminal font.
```

Mention these specifics in the bug or sponsor notes:

- this is a fonts package, not an application;
- the package installs only Nerd Fonts Symbols Only assets;
- the fontconfig snippet is upstream-provided by Nerd Fonts;
- normal text continues to render with the user's selected monospace font;
- `Symbols Nerd Font` is only a fallback for missing icon/private-use glyphs;
- the intended install paths are under `/usr/share/fonts/truetype/nerd-fonts-symbols/`, `/usr/share/fontconfig/conf.avail/`, and `/etc/fonts/conf.d/`.

## Changelog for Debian

After the ITP exists, update `debian/changelog` on the Debian branch:

```text
fonts-nerd-symbols (3.4.0-1) unstable; urgency=medium

  * Initial release. (Closes: #NNNNNN)

 -- Marlen Brunner <klondikemarlen+debian@gmail.com>  Wed, 08 Jul 2026 14:08:46 -0700
```

Use the public Debian packaging email you used for the ITP. Do not change the PPA branch from `resolute` to `unstable`; keep Debian submission work separate.

## Build source for review

Build Debian uploads in Debian, not Ubuntu. Ubuntu's `lintian` can reject `Distribution: unstable`, and Ubuntu-built source metadata can include Ubuntu-specific build context.

A disposable Debian container is enough for this package:

```bash
docker run --rm -v "$PWD:/work" -w /work debian:unstable sh -lc '
  set -eu
  export DEBIAN_FRONTEND=noninteractive
  apt-get update >/dev/null
  apt-get install -y --no-install-recommends \
    ca-certificates wget unzip xz-utils dpkg-dev devscripts debhelper lintian build-essential >/dev/null
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
debsign -kFULL_FINGERPRINT build/fonts-nerd-symbols_3.4.0-1_source.changes
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
dput mentors build/fonts-nerd-symbols_3.4.0-1_source.changes
```

If the `mentors` dput profile is missing, use the mentors.debian.net web upload or add the mentors upload profile from their maintainer instructions.

After mentors accepts the upload, it sends the public package page, `.dsc` URL, and an RFS helper URL. Use those links in the sponsorship request instead of guessing paths.

## Submit for sponsorship

After mentors accepts the upload and shows a package page, file an RFS bug.

Typical RFS subject:

```text
RFS: fonts-nerd-symbols/3.4.0-1 [ITP] -- Nerd Fonts symbols fallback for fontconfig
```

Include the ITP bug number, mentors package URL, source package URL, lintian result, and a short note that this is a fonts/fontconfig fallback package.

Sponsor review will focus on licensing, source/orig tarball construction, Debian font paths, fontconfig behavior, lintian output, and whether generated/binary font assets are handled according to Debian policy.
