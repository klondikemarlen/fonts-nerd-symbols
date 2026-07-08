# Official Debian/Ubuntu archive path

This is the path to `sudo apt install fonts-nerd-symbols` without adding a PPA or downloading a `.deb`. Do this on a separate branch so PPA work on `main` can keep targeting Ubuntu series such as `resolute`.

```bash
git checkout -b debian-submission
```

## Debian-first path

Recommended flow:

1. File an ITP bug for `fonts-nerd-symbols`.
2. Update `debian/changelog` to close it: `Closes: #NNNNNN`.
3. Set the changelog distribution to `unstable` on the Debian submission branch.
4. Build a signed source package with `debuild -S -sa` for a new upstream orig tarball, or `debuild -S -sd` for later Debian revisions of the same upstream version.
5. Run `lintian` on the source `.changes` and `.dsc`.
6. Upload to mentors.debian.net.
7. File an RFS bug and find a Debian sponsor.
8. Pass Debian NEW review.
9. Ubuntu can later sync the package from Debian.

## Filing the ITP

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

## Ubuntu-direct path

If you skip Debian, file a Launchpad bug/package request for Ubuntu, attach or link the source package, find an Ubuntu sponsor, and pass Ubuntu archive review. Debian-first is cleaner for this package.

## Policy notes

- Keep the upstream font binaries out of git.
- Generate the upstream `orig.tar.xz` from the Nerd Fonts release asset.
- Keep managed fontconfig snippets under `/usr/share/fontconfig/conf.avail/`.
- Enable the snippet with an `/etc/fonts/conf.d/10-nerd-font-symbols.conf` symlink.
- Upload source packages to PPAs/archive, not hand-built binary `.deb` files.
- Never commit `~/.gnupg`, private keys, passphrases, Launchpad confirmation emails, or upload credentials.
