# Debian-first package submission

Use this path when you want `fonts-nerd-symbols` to become an official Debian package first, then flow into Ubuntu by normal sync.

Use `debian/latest` as the long-lived Debian packaging branch. Keep PPA/GitHub release work on `main` so Ubuntu series changelog targets such as `resolute` do not accidentally switch to `unstable`.

## Flow

1. File an ITP bug for `fonts-nerd-symbols`.
2. Update `debian/changelog` to close it: `Closes: #NNNNNN`.
3. Set the changelog distribution to `unstable` on the Debian packaging branch.
4. Build a signed source package with `debuild -S -sa` for a new upstream orig tarball, or `debuild -S -sd` for later Debian revisions of the same upstream version.
5. Run `lintian` on the source `.changes` and `.dsc`.
6. Upload to mentors.debian.net.
7. File an RFS bug against `sponsorship-requests` by sending the mentors RFS template to `submit@bugs.debian.org`.
8. Pass Debian NEW review.
9. Ubuntu can later sync the package from Debian.

## File the ITP

```bash
sudo apt install reportbug
reportbug wnpp
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

Current Debian tracker state:

```text
ITP: #1141696
RFS: #1141699
Current mentors upload: fonts-nerd-symbols_3.4.0-2
```

For a future first upload of a new package, after the ITP exists, update `debian/changelog` on the Debian branch:

```text
fonts-nerd-symbols (NEXT_VERSION) unstable; urgency=medium

  * Initial release. (Closes: #NNNNNN)

 -- Marlen Brunner <klondikemarlen+debian@gmail.com>  DATE
```

Do not change the PPA branch from `resolute` to `unstable`; keep Debian submission work on `debian/latest`.

## Build source for review

```bash
sudo apt install devscripts debhelper lintian
rm -rf build
UPSTREAM_VERSION="$(dpkg-parsechangelog -S Version | sed 's/-[^-]*$//')"
SOURCE_VERSION="$(dpkg-parsechangelog -S Version)"
./debian/scripts/prepare-upstream "$UPSTREAM_VERSION"
cd "build/fonts-nerd-symbols-$UPSTREAM_VERSION"
debuild -S -sa
lintian "../fonts-nerd-symbols_${SOURCE_VERSION}_source.changes" "../fonts-nerd-symbols_${SOURCE_VERSION}.dsc"
```

Use `-sa` for the first Debian upload of a new upstream orig tarball. Use `-sd` only for later Debian revisions of the same upstream version after the orig tarball is already in the target archive.

## Submit for sponsorship

Upload the signed source package to <https://mentors.debian.net/>, then file an RFS bug against `sponsorship-requests`.

For the initial Debian submission of this package:

```text
ITP: #1141696
RFS: #1141699
Mentors upload: fonts-nerd-symbols_3.4.0-2
DSC: https://mentors.debian.net/debian/pool/main/f/fonts-nerd-symbols/fonts-nerd-symbols_3.4.0-2.dsc
Debian packaging branch: https://github.com/klondikemarlen/fonts-nerd-symbols/tree/debian/latest
```

Typical RFS subject:

```text
RFS: fonts-nerd-symbols/3.4.0-2 [ITP] -- Nerd Fonts symbols fallback for fontconfig
```

Sponsor review will focus on licensing, source/orig tarball construction, Debian font paths, fontconfig behavior, lintian output, and whether generated/binary font assets are handled according to Debian policy.
