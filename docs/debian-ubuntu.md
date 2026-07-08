# Official Debian/Ubuntu archive path

This is the path to `sudo apt install fonts-nerd-symbols` without adding a PPA or downloading a `.deb`.

## Guides

- [Debian-first package submission](debian-first.md)
- Ubuntu-direct package request: see below.
- Package policy notes: see below.

## Ubuntu-direct path

If you skip Debian, file a Launchpad bug/package request for Ubuntu, attach or link the source package, find an Ubuntu sponsor, and pass Ubuntu archive review. Debian-first is cleaner for this package.

## Policy notes

- Keep the upstream font binaries out of git.
- Generate the upstream `orig.tar.xz` from the Nerd Fonts release asset.
- Keep managed fontconfig snippets under `/usr/share/fontconfig/conf.avail/`.
- Enable the snippet with an `/etc/fonts/conf.d/10-nerd-font-symbols.conf` symlink.
- Upload source packages to PPAs/archive, not hand-built binary `.deb` files.
- Never commit `~/.gnupg`, private keys, passphrases, Launchpad confirmation emails, or upload credentials.
