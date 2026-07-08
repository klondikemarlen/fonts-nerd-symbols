# Install and verify

## Fast two-command install

```bash
wget https://github.com/klondikemarlen/fonts-nerd-symbols/releases/latest/download/fonts-nerd-symbols_all.deb
sudo apt install ./fonts-nerd-symbols_all.deb
```

## PPA install for apt-managed updates

```bash
sudo add-apt-repository ppa:klondikemarlen/fonts-nerd-symbols
sudo apt update
sudo apt install fonts-nerd-symbols
```

## Verify apt source

```bash
apt-cache policy fonts-nerd-symbols
```

For PPA installs, the version table should include:

```text
https://ppa.launchpadcontent.net/klondikemarlen/fonts-nerd-symbols/ubuntu
```

## Verify installed files

```bash
dpkg -L fonts-nerd-symbols
fc-match 'Symbols Nerd Font'
echo "Nerd Font test:    "
```

Expected installed files include:

```text
/usr/share/fonts/truetype/nerd-fonts-symbols/SymbolsNerdFont-Regular.ttf
/usr/share/fonts/truetype/nerd-fonts-symbols/SymbolsNerdFontMono-Regular.ttf
/usr/share/fontconfig/conf.avail/10-nerd-font-symbols.conf
/etc/fonts/conf.d/10-nerd-font-symbols.conf
```

## Scope

This package is broad, but not universal. It helps apps that honor fontconfig fallback. It does not patch every font or force apps that insist on a single font to use fallback glyphs.
