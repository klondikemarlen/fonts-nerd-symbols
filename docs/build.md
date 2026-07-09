# Build and release

No private keys, passphrases, Launchpad tokens, GitHub tokens, encrypted email contents, or GPG secret-key exports belong in this repository.

## Install build tools

```bash
sudo apt install git xz-utils build-essential devscripts debhelper lintian dput fontforge python3-fontforge fontconfig
```

## Version variables

Before each release, update `debian/changelog`, then derive versions from it:

```bash
UPSTREAM_VERSION="$(dpkg-parsechangelog -S Version | sed 's/-[^-]*$//')"
SOURCE_VERSION="$(dpkg-parsechangelog -S Version)"
```

## Build DFSG package

This branch builds only the Debian-clean `+dfsg` package. It rebuilds Symbols
Nerd Font from source inputs and excludes Font Logos.

```bash
./debian/scripts/build-dfsg-package
```

For a different release, pass the source version and distribution as arguments:
`./debian/scripts/build-dfsg-package "$SOURCE_VERSION" unstable`.

## Unsigned source package for local checking

Use `-sa` when the orig tarball identity is new, including the first `+dfsg` repack upload. Use `-sd` only for later Debian revisions that reuse an already-uploaded orig tarball unchanged.

```bash
debuild -S -sa -us -uc
lintian "../fonts-nerd-symbols_${SOURCE_VERSION}_source.changes" "../fonts-nerd-symbols_${SOURCE_VERSION}.dsc"
```

## GitHub release assets

From `build/`:

```bash
cp "fonts-nerd-symbols_${SOURCE_VERSION}_all.deb" fonts-nerd-symbols_all.deb
sha256sum \
  "fonts-nerd-symbols_${SOURCE_VERSION}_all.deb" \
  fonts-nerd-symbols_all.deb \
  "fonts-nerd-symbols_${SOURCE_VERSION}.dsc" \
  "fonts-nerd-symbols_${SOURCE_VERSION}.debian.tar.xz" \
  "fonts-nerd-symbols_${UPSTREAM_VERSION}.orig.tar.xz" \
  "fonts-nerd-symbols_${SOURCE_VERSION}_source.changes" \
  > SHA256SUMS
```

Attach:

```text
fonts-nerd-symbols_all.deb
fonts-nerd-symbols_${SOURCE_VERSION}_all.deb
fonts-nerd-symbols_${SOURCE_VERSION}.dsc
fonts-nerd-symbols_${SOURCE_VERSION}.debian.tar.xz
fonts-nerd-symbols_${UPSTREAM_VERSION}.orig.tar.xz
fonts-nerd-symbols_${SOURCE_VERSION}_source.changes
SHA256SUMS
```

The stable alias `fonts-nerd-symbols_all.deb` backs the two-command install URL.
