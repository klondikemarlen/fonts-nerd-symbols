# fonts-nerd-symbols

Debian/Ubuntu package for Nerd Fonts' **Symbols Only** fontconfig fallback.

The package keeps your normal terminal font, such as `Ubuntu Sans Mono`, and uses `Symbols Nerd Font` only for missing Nerd Font icon glyphs. That avoids switching the whole terminal to a patched Nerd Font.

## Install

Fast two-command install:

```bash
wget https://github.com/klondikemarlen/fonts-nerd-symbols/releases/latest/download/fonts-nerd-symbols_all.deb
sudo apt install ./fonts-nerd-symbols_all.deb
```

PPA install for apt-managed updates:

```bash
sudo add-apt-repository ppa:klondikemarlen/fonts-nerd-symbols
sudo apt update
sudo apt install fonts-nerd-symbols
```

## Docs

- [Docs index](docs/README.md)
- [Install and verify](docs/install.md)
- [Build and release](docs/build.md)
- [Launchpad PPA publishing](docs/launchpad-ppa.md)
- [Official Debian/Ubuntu archive path](docs/debian-ubuntu.md)
- [Debian-first package submission](docs/debian-first.md)
- [Ubuntu-direct package request](docs/ubuntu-direct.md)

## What it installs

```text
/usr/share/fonts/truetype/nerd-fonts-symbols/SymbolsNerdFont-Regular.ttf
/usr/share/fonts/truetype/nerd-fonts-symbols/SymbolsNerdFontMono-Regular.ttf
/usr/share/fontconfig/conf.avail/10-nerd-font-symbols.conf
/etc/fonts/conf.d/10-nerd-font-symbols.conf -> /usr/share/fontconfig/conf.avail/10-nerd-font-symbols.conf
```

## Upstream

- Nerd Fonts: <https://github.com/ryanoasis/nerd-fonts>
- Symbols Only release asset: <https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/NerdFontsSymbolsOnly.zip>
