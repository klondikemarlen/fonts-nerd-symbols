# Build and release

No private keys, passphrases, Launchpad tokens, GitHub tokens, encrypted email contents, or GPG secret-key exports belong in this repository.

## Pull request review and QA

Before release, link the change to an issue and open a draft pull request against its target branch. The author must review the complete diff and add a PR comment recording every finding, any fixup, and a `PASS`, `FAIL`, or `BLOCKED` result.

Run targeted QA and the smallest relevant automated check, then post the exact scenario, command, and outcome in the PR. Resolve every actionable comment before merging. After any fix, repeat the complete self-review and QA and post the new evidence; keep the PR blocked until comments and checks are resolved.

## Install build tools

```bash
sudo apt install git xz-utils build-essential devscripts debhelper lintian dput sbuild sbuild-schroot debootstrap schroot fontforge python3-fontforge fontconfig
```

## Version variables

Before each release, update `debian/changelog`, then derive versions from it:

```bash
UPSTREAM_VERSION="$(dpkg-parsechangelog -S Version | sed 's/-[^-]*$//')"
SOURCE_VERSION="$(dpkg-parsechangelog -S Version)"
```

## Prepare DFSG source tree

The default build is the Debian-clean `+dfsg` package. It rebuilds Symbols
Nerd Font from source inputs and excludes Font Logos.

```bash
./debian/scripts/build-dfsg-package
```

For a different release, pass the source version and distribution as arguments:
`./debian/scripts/build-dfsg-package "$SOURCE_VERSION" resolute`.

## Local full-symbols package

This is an explicit local/manual helper for reproducing the old all-symbols
package shape, including Font Logos. Do not use it for Debian uploads, and do
not publish it to the same PPA/release line unless you first choose a separate
package/versioning scheme.

```bash
./debian/scripts/build-full-package 3.4.0 3.4.0-4~full1 resolute
```

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
