# Ubuntu registration path

This package has three publication levels.

## Current level: GitHub Release `.deb`

Use this for the simple public install flow:

```bash
wget https://github.com/klondikemarlen/fonts-nerd-symbols/releases/latest/download/fonts-nerd-symbols_all.deb
sudo apt install ./fonts-nerd-symbols_all.deb
```

This is findable and easy, but it is not Ubuntu-verified and does not provide automatic apt updates.

## Next level: Launchpad PPA

A PPA takes a signed source package, not the binary `.deb`.

1. Create a Launchpad account if needed.
2. Add and confirm your GPG key in Launchpad.
3. Create a PPA named `fonts-nerd-symbols`.
4. Build a signed source upload:

```bash
./debian/scripts/prepare-upstream 3.4.0
cd build/fonts-nerd-symbols-3.4.0
debuild -S -sa
```

5. Upload it:

```bash
dput ppa:klondikemarlen/fonts-nerd-symbols ../fonts-nerd-symbols_3.4.0-1_source.changes
```

After Launchpad builds it, users install with:

```bash
sudo add-apt-repository ppa:klondikemarlen/fonts-nerd-symbols
sudo apt install fonts-nerd-symbols
```

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
- Enable the snippet with `/etc/fonts/conf.d/10-nerd-font-symbols.conf` symlink.
- Upload source packages to PPAs/archive, not hand-built binary `.deb` files.
