# Package policy notes

Use this checklist before uploading to a PPA, Debian, or Ubuntu.

## Source and repository hygiene

Keep generated or upstream binary font files out of git. The repository should carry Debian packaging, scripts, docs, and metadata, not unpacked release assets.

Never commit:

- `~/.gnupg`;
- private keys or secret-key exports;
- passphrases;
- Launchpad confirmation emails;
- decrypted Launchpad confirmations;
- Launchpad tokens;
- GitHub tokens;
- upload credentials.

## Upstream orig tarball

Generate the upstream `orig.tar.xz` from the Nerd Fonts Symbols Only release asset:

```text
https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/NerdFontsSymbolsOnly.zip
```

The orig tarball should carry upstream content only. Debian packaging belongs in the Debian tarball/source package layer, not inside the upstream orig content.

Keep the orig tarball reproducible across Debian revisions of the same upstream version. Launchpad and Debian reject changed contents for the same source version/orig tarball identity. If a package upload is broken, upload a higher Debian revision instead of mutating an existing source version.

## Font install paths

Install font files under:

```text
/usr/share/fonts/truetype/nerd-fonts-symbols/
```

Expected files:

```text
SymbolsNerdFont-Regular.ttf
SymbolsNerdFontMono-Regular.ttf
```

## Fontconfig install paths

Keep managed fontconfig snippets under:

```text
/usr/share/fontconfig/conf.avail/
```

Enable the snippet through:

```text
/etc/fonts/conf.d/10-nerd-font-symbols.conf -> /usr/share/fontconfig/conf.avail/10-nerd-font-symbols.conf
```

The package should not require users to manually copy config files after installation.

## Binary packages versus source uploads

GitHub releases may provide a convenient binary `.deb` for direct installs. PPAs, Debian, and Ubuntu archive uploads should receive signed source packages, not hand-built binary `.deb` files.

Use:

```text
.dsc
.debian.tar.xz
.orig.tar.xz
_source.changes
```

Do not submit only:

```text
fonts-nerd-symbols_all.deb
```

## Changelog targets

Use the right distribution target for the destination:

```text
resolute   # Ubuntu PPA/archive target for that Ubuntu series
unstable   # Debian submission target
```

Keep Debian submission work on its own branch so PPA release work does not accidentally switch to `unstable`.

## Smoke checks

After installing a built package, verify:

```bash
dpkg -L fonts-nerd-symbols
fc-match 'Symbols Nerd Font'
echo "Nerd Font test:    "
```

For PPA installs, also verify:

```bash
apt-cache policy fonts-nerd-symbols
```

The policy output should show the PPA or archive source that provided the installed version.
