# fonts-nerd-symbols

Debian/Ubuntu source package for Nerd Fonts' **Symbols Only** fontconfig fallback.

The package keeps your normal terminal font, such as `Ubuntu Sans Mono`, and uses `Symbols Nerd Font` only for missing Nerd Font icon glyphs. That avoids switching the whole terminal to a patched Nerd Font.

## Install

Target public install flow:

```bash
wget https://github.com/klondikemarlen/fonts-nerd-symbols/releases/latest/download/fonts-nerd-symbols_all.deb
sudo apt install ./fonts-nerd-symbols_all.deb
```

Restart the terminal, keep your terminal font set to `Ubuntu Sans Mono`, then test:

```bash
echo "Nerd Font test:    "
```

## What it installs

```text
/usr/share/fonts/truetype/nerd-fonts-symbols/SymbolsNerdFont-Regular.ttf
/usr/share/fonts/truetype/nerd-fonts-symbols/SymbolsNerdFontMono-Regular.ttf
/usr/share/fontconfig/conf.avail/10-nerd-font-symbols.conf
/etc/fonts/conf.d/10-nerd-font-symbols.conf -> /usr/share/fontconfig/conf.avail/10-nerd-font-symbols.conf
```

## Build locally

Install packaging tools:

```bash
sudo apt install devscripts debhelper lintian
```

Prepare the upstream orig tarball and Debian source tree:

```bash
debian/rules get-orig-source
```

Build the binary and source package:

```bash
cd build/fonts-nerd-symbols-3.4.0
debuild -us -uc
```

Build the source-only upload and run lintian:

```bash
debuild -S -sa -us -uc
lintian ../fonts-nerd-symbols_3.4.0-1_source.changes ../fonts-nerd-symbols_3.4.0-1.dsc
```

## Ubuntu/Debian inclusion path

This repository is structured around a Debian source package, not a hand-built binary dump. The learning path is:

1. keep `debian/` policy-clean;
2. create an upstream `orig.tar.*` from the Nerd Fonts Symbols Only release;
3. build with `debuild` / `dpkg-buildpackage`;
4. check with `lintian`;
5. publish `.deb` releases for easy two-command install;
6. later, prepare a source upload through a PPA, Debian sponsor, or Ubuntu packaging process.

Official Ubuntu availability requires source-package review and archive inclusion. A GitHub `.deb` is convenient, but it is not Ubuntu-verified.

See [docs/ubuntu-registration.md](docs/ubuntu-registration.md) for the PPA and official Ubuntu/Debian archive path.

## Upstream

- Nerd Fonts: <https://github.com/ryanoasis/nerd-fonts>
- Symbols Only release asset: <https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/NerdFontsSymbolsOnly.zip>
