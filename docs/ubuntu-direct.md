# Ubuntu-direct package request

Use this path only if you want Ubuntu archive inclusion before, or instead of, Debian inclusion. Debian-first is still the cleaner path for this package.

## What Ubuntu-direct means

A PPA is not Ubuntu archive inclusion. A PPA gives users an apt source under your Launchpad account. Ubuntu-direct means getting `fonts-nerd-symbols` reviewed and accepted into Ubuntu's official archive so users can install it from Ubuntu repositories without adding your PPA.

## Flow

1. File a Launchpad bug/package request for `fonts-nerd-symbols`.
2. Attach or link the signed Debian source package artifacts.
3. Explain why the package is useful for Ubuntu users.
4. Find an Ubuntu sponsor.
5. Address sponsor/archive-review feedback.
6. Pass Ubuntu archive review.
7. Once accepted, users can install with `sudo apt install fonts-nerd-symbols` from Ubuntu repositories.

## Package request details

Use a Launchpad bug against Ubuntu. Include:

```text
Package name: fonts-nerd-symbols
Summary: Nerd Fonts symbols fallback for fontconfig
Upstream: https://github.com/ryanoasis/nerd-fonts
Packaging: https://github.com/klondikemarlen/fonts-nerd-symbols
License: pending DFSG/provenance audit
```

Describe the Ubuntu-specific value:

```text
Ubuntu terminal users can keep Ubuntu Sans Mono or another normal monospace
font while fontconfig falls back to Symbols Nerd Font for missing Nerd Font
icon glyphs. This fixes terminal icon rendering without requiring users to
switch their whole terminal font to a patched Nerd Font face.
```

Include concrete package behavior:

```text
Installs SymbolsNerdFont-Regular.ttf and SymbolsNerdFontMono-Regular.ttf under
/usr/share/fonts/truetype/nerd-fonts-symbols/. Installs the upstream Nerd Fonts
fontconfig alias file under /usr/share/fontconfig/conf.avail/ and enables it
through /etc/fonts/conf.d/10-nerd-font-symbols.conf.
```

## Source package artifacts

Upload or link source package artifacts, not a hand-built binary `.deb`:

```text
fonts-nerd-symbols_${SOURCE_VERSION}.dsc
fonts-nerd-symbols_${SOURCE_VERSION}.debian.tar.xz
fonts-nerd-symbols_${UPSTREAM_VERSION}.orig.tar.xz
fonts-nerd-symbols_${SOURCE_VERSION}_source.changes
```

The GitHub release may host these artifacts, but the official review still cares about the signed source package and Debian/Ubuntu policy compliance.

Before requesting Ubuntu archive review, complete the same DFSG/provenance audit required for Debian: document each included Symbols Only glyph source, license, and preferred form for modification, or rebuild/repack without doubtful glyph sets.

## Changelog target

For Ubuntu-direct work, use the target Ubuntu series, for example:

```text
fonts-nerd-symbols (3.4.0-1) resolute; urgency=medium
```

Do not use `unstable` for an Ubuntu PPA/archive upload. `unstable` is the Debian target.

## Find a sponsor

Ubuntu archive uploads require a sponsor unless you have upload rights. Give the sponsor:

- Launchpad bug URL;
- source package artifacts;
- lintian output;
- explanation of upstream source generation and DFSG/provenance audit status;
- package install paths;
- fontconfig behavior;
- why this is not just a local PPA package.

## Prefer Debian-first when possible

For this package, Debian-first avoids a permanent Ubuntu-only packaging delta. Once accepted in Debian, Ubuntu can sync it and future maintenance is simpler.
