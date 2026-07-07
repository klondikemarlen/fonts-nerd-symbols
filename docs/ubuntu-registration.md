# Ubuntu registration path

This document records the repeatable publication process for `fonts-nerd-symbols`.

No private keys, passphrases, Launchpad tokens, GitHub tokens, encrypted email contents, or GPG secret-key exports belong in this repository.

## Release version variables

Before each new release, update `debian/changelog`, then derive the versions from it:

```bash
UPSTREAM_VERSION="$(dpkg-parsechangelog -S Version | sed 's/-[^-]*$//')"
SOURCE_VERSION="$(dpkg-parsechangelog -S Version)"
```

Examples in this document assume the current release is `3.4.0-1`; for future releases, use the values above instead of hardcoding versions.

## Current level: GitHub Release `.deb`

Use this for the simple public two-command install flow:

```bash
wget https://github.com/klondikemarlen/fonts-nerd-symbols/releases/latest/download/fonts-nerd-symbols_all.deb
sudo apt install ./fonts-nerd-symbols_all.deb
```

This is findable and easy, but it is not Ubuntu-verified and does not provide automatic apt updates.

## One-time Launchpad setup

### 1. Create a GPG key with signing and encryption capability

Use GPG for package signing. SSH keys do not sign Debian source uploads.

```bash
gpg --quick-generate-key "Marlen Brunner <klondikemarlen@gmail.com>" rsa4096 default 2y
```

If the key only shows `[SC]` and has no encryption subkey, add one using the full fingerprint:

```bash
gpg --quick-add-key FULL_FINGERPRINT rsa4096 encr 2y
```

Verify the key has signing/certification and an encryption subkey:

```bash
gpg --list-secret-keys --keyid-format=long --with-subkey-fingerprint
```

Expected shape:

```text
sec   rsa4096/KEY_ID ... [SC]
      FULL_FINGERPRINT
uid   ... Marlen Brunner <klondikemarlen@gmail.com>
ssb   rsa4096/SUBKEY_ID ... [E]
      SUBKEY_FINGERPRINT
```

### 2. Publish the public key to Ubuntu's keyserver

```bash
gpg --keyserver keyserver.ubuntu.com --send-keys FULL_FINGERPRINT
```

Keyserver visibility can lag. Wait 10-30 minutes if Launchpad cannot find it immediately.

### 3. Import the key in Launchpad

Go to:

```text
https://launchpad.net/~/+editpgpkeys
```

Paste the full fingerprint, not the short key ID.

Launchpad may send an encrypted confirmation email. Copy the full PGP message block into a local file and decrypt it locally:

```bash
gpg --decrypt /tmp/launchpad-key-confirmation.asc
```

Follow the confirmation link/instructions from the decrypted message.

Do not commit the encrypted email, decrypted confirmation, or any private key material.

### 4. Create the PPA

From your Launchpad profile, create a Personal Package Archive.

Use:

```text
URL/name: fonts-nerd-symbols
Display name: Nerd Font Symbols
Description: Symbols Nerd Font fallback package for Ubuntu fontconfig. Lets Ubuntu Sans Mono and other normal terminal fonts render Nerd Font icon glyphs without switching the whole terminal font.
```

Do not put `/ubuntu` in the PPA name. Launchpad adds that path for apt repository URLs later.

## Upload to the Launchpad PPA

A PPA takes a signed source package, not the binary `.deb`.

Install the needed upload/build tools:

```bash
sudo apt install devscripts debhelper lintian dput
```

From the repository root:

```bash
rm -rf build
./debian/scripts/prepare-upstream "$UPSTREAM_VERSION"
cd "build/fonts-nerd-symbols-$UPSTREAM_VERSION"
debuild -S -sa
```

Important: do not use `-us -uc` for a real upload. Those flags skip signing.

Run lintian on the signed source upload:

```bash
lintian "../fonts-nerd-symbols_${SOURCE_VERSION}_source.changes" "../fonts-nerd-symbols_${SOURCE_VERSION}.dsc"
```

Upload to the PPA:

```bash
dput ppa:klondikemarlen/fonts-nerd-symbols "../fonts-nerd-symbols_${SOURCE_VERSION}_source.changes"
```

After upload, refresh:

```text
https://launchpad.net/~klondikemarlen/+archive/ubuntu/fonts-nerd-symbols
```

Launchpad should show the upload as pending, then building, then published.

After Launchpad publishes it, users install with:

```bash
sudo add-apt-repository ppa:klondikemarlen/fonts-nerd-symbols
sudo apt install fonts-nerd-symbols
```

## GitHub release build process

Use this when publishing a direct `.deb` release.

```bash
rm -rf build
./debian/scripts/prepare-upstream "$UPSTREAM_VERSION"
cd "build/fonts-nerd-symbols-$UPSTREAM_VERSION"
debuild -us -uc
debuild -S -sa -us -uc
cd ..
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

For GitHub Releases, attach:

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

## Final level: Debian/Ubuntu archive

This is the only path to `sudo apt install fonts-nerd-symbols` without adding a PPA or downloading a `.deb`.

Debian-first path:

1. File an ITP bug for `fonts-nerd-symbols`.
2. Update `debian/changelog` to close it: `Closes: #NNNNNN`.
3. Build a signed source package with `debuild -S -sa`.
4. Run `lintian` on the source `.changes` and `.dsc`.
5. Find a Debian sponsor.
6. Upload to Debian NEW queue.
7. Wait for review and acceptance.
8. Ubuntu can later sync the package from Debian.

Ubuntu-direct path:

1. File a Launchpad bug/package request.
2. Attach or link the source package.
3. Find an Ubuntu sponsor.
4. Pass Ubuntu archive review.

## Package policy notes

- Keep the upstream font binaries out of git.
- Generate the upstream `orig.tar.xz` from the Nerd Fonts release asset.
- Keep managed fontconfig snippets under `/usr/share/fontconfig/conf.avail/`.
- Enable the snippet with an `/etc/fonts/conf.d/10-nerd-font-symbols.conf` symlink.
- Upload source packages to PPAs/archive, not hand-built binary `.deb` files.
- Never commit `~/.gnupg`, private keys, passphrases, Launchpad confirmation emails, or upload credentials.
