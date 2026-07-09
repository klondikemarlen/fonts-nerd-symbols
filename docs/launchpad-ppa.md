# Launchpad PPA publishing

No private keys, passphrases, Launchpad tokens, GitHub tokens, encrypted email contents, or GPG secret-key exports belong in this repository.

## One-time GPG setup

Use GPG for package signing. SSH keys do not sign Debian source uploads.

```bash
gpg --quick-generate-key "Marlen Brunner <klondikemarlen@gmail.com>" rsa4096 default 2y
```

If the key only shows `[SC]` and has no encryption subkey, add one using the full fingerprint:

```bash
gpg --quick-add-key FULL_FINGERPRINT rsa4096 encr 2y
```

Verify:

```bash
gpg --list-secret-keys --keyid-format=long --with-subkey-fingerprint
```

Publish the public key to Ubuntu's keyserver:

```bash
gpg --keyserver keyserver.ubuntu.com --send-keys FULL_FINGERPRINT
```

Import the key in Launchpad:

```text
https://launchpad.net/~/+editpgpkeys
```

Paste the full fingerprint, not the short key ID. Launchpad may send an encrypted confirmation email; decrypt it locally with `gpg --decrypt`. Do not commit the encrypted email, decrypted confirmation, or any private key material.

## Create the PPA

From your Launchpad profile, create a Personal Package Archive:

```text
URL/name: fonts-nerd-symbols
Display name: Nerd Font Symbols
Description: Symbols Nerd Font fallback package for Ubuntu fontconfig. Lets Ubuntu Sans Mono and other normal terminal fonts render Nerd Font icon glyphs without switching the whole terminal font.
```

Do not put `/ubuntu` in the PPA name. Launchpad adds that path for apt repository URLs later.

## Upload to the PPA

A PPA takes a signed source package, not the binary `.deb`.

```bash
sudo apt install devscripts debhelper lintian dput
rm -rf build
UPSTREAM_VERSION="$(dpkg-parsechangelog -S Version | sed 's/-[^-]*$//')"
SOURCE_VERSION="$(dpkg-parsechangelog -S Version)"
./debian/scripts/prepare-upstream "$UPSTREAM_VERSION"
cd "build/fonts-nerd-symbols-$UPSTREAM_VERSION"
```

Build the signed source upload. Use `-sa` when the orig tarball identity is new, including `+dfsg` repacks. Use `-sd` only for later Debian revisions that reuse an already-uploaded orig tarball unchanged.

```bash
debuild -S -sa
lintian "../fonts-nerd-symbols_${SOURCE_VERSION}_source.changes" "../fonts-nerd-symbols_${SOURCE_VERSION}.dsc"
dput ppa:klondikemarlen/fonts-nerd-symbols "../fonts-nerd-symbols_${SOURCE_VERSION}_source.changes"
```

## Publication check

Launchpad should show the upload as pending, then building, then published. The apt repository is usable only after the InRelease metadata is published:

```bash
curl -I https://ppa.launchpadcontent.net/klondikemarlen/fonts-nerd-symbols/ubuntu/dists/resolute/InRelease
```

Ready means `HTTP 200`. Not ready means `403 Forbidden`; wait for Launchpad's publisher.

## Install from PPA

```bash
sudo add-apt-repository ppa:klondikemarlen/fonts-nerd-symbols
sudo apt update
sudo apt install fonts-nerd-symbols
apt-cache policy fonts-nerd-symbols
```

`apt-cache policy` should show `https://ppa.launchpadcontent.net/klondikemarlen/fonts-nerd-symbols/ubuntu` as a source.

## Delete broken PPA package versions

Official docs: <https://ubuntu.com/docs/launchpad/user/how-to/packaging/deleting-packages/>

Launchpad can delete packages from a PPA:

1. Open the PPA page.
2. Click **View package details**.
3. Click **Delete packages**.
4. Search/select the package version.
5. Add a deletion comment.
6. Request deletion.

Deletion affects the selected source package and any binaries built from it.

Timing:

- archive indexes: removed in at most about 20 minutes;
- files on disk: cleanup job runs about every six hours;
- deleted files may remain recoverable by file link for up to seven days.

Important: deletion does not let you re-upload the same source version with different contents. Replace broken packages by uploading a higher Debian revision instead, for example `3.4.0-3` after `3.4.0-1` failed.

Failed build history may still appear in Launchpad build records even after package deletion. Treat that as audit history; clean the published package list if Launchpad offers deletion, but do not fight immutable build logs.
