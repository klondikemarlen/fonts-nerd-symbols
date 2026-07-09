# DFSG glyph provenance audit

Issue: https://github.com/klondikemarlen/fonts-nerd-symbols/issues/1

This package now rebuilds Symbols Nerd Font from the Nerd Fonts v3.4.0 source inputs in `upstream-src/` and intentionally omits the `--fontlogos` patcher option. Upstream's `bin/scripts/lib/i_all.sh` includes `logos` in the all-symbols build, but upstream `license-audit.md` lists Font Logos as `Unlicensed`, and Debian's Nerd Fonts wiki flags logo glyphs as likely non-distributable. The Debian-clean build excludes that glyph set and does not ship `src/glyphs/font-logos.ttf` or `bin/scripts/lib/i_logos.sh` in the orig source.

## Rebuild inputs

- Template: `src/unpatched-fonts/NerdFontsSymbolsOnly/NerdFontsSymbolsNerdFontBlank.sfd`
- Seti/custom preferred source: `src/svgs/`, regenerated through `bin/scripts/generate-original-source.py`
- Glyph sources: `src/glyphs/`
- Patcher: `font-patcher`
- Enabled patcher flags: `--codicons --fontawesome --fontawesomeext --octicons --powersymbols --pomicons --powerline --powerlineextra --material --weather`
- Deliberately omitted patcher flag: `--fontlogos`

## Audit table

| Glyph set | Upstream/source in orig | License | Preferred modification form | DFSG decision | Notes |
| --- | --- | --- | --- | --- | --- |
| Seti UI + Custom | `upstream-src/src/svgs/`, `upstream-src/bin/scripts/generate-original-source.py` | MIT, per Nerd Fonts `license-audit.md` as Original Source / Seti-UI modified | SVG files plus generator; `original-source.otf` is regenerated during build | Keep | `font-patcher` enables this unconditionally. |
| Devicons | `upstream-src/src/glyphs/devicons/` | MIT | SVG/font sources and mapping scripts in `src/glyphs/devicons/` | Keep | `font-patcher` enables this unconditionally. |
| Font Awesome | `upstream-src/src/glyphs/font-awesome/` | CC BY 4.0 for icons / OFL 1.1 for font files | FontAwesome OTF plus upstream mapping/generate scripts | Keep | DFSG-free; attribution/license retained. |
| Font Awesome Extension | `upstream-src/src/glyphs/font-awesome-extension.ttf` | MIT | Upstream glyph font | Keep | Included by `--fontawesomeext`. |
| Material Design Icons | `upstream-src/src/glyphs/materialdesign/` | Apache-2.0 | MaterialDesignIconsDesktop TTF plus README/source notes | Keep | Included by `--material`. |
| Weather Icons | `upstream-src/src/glyphs/weather-icons/` | SIL OFL 1.1 | Weather Icons webfont plus OFL files | Keep | Included by `--weather`. |
| Octicons | `upstream-src/src/glyphs/octicons/` | MIT | Octicons OTF/SVG fixes plus mapping/generate scripts | Keep | Included by `--octicons`. |
| Font Logos | Not shipped; `src/glyphs/font-logos.ttf` and `bin/scripts/lib/i_logos.sh` are removed in `prepare-upstream` | Upstream `license-audit.md`: Unlicensed | N/A | Exclude | Debian wiki flags logo glyphs as likely non-distributable; build omits `--fontlogos`. |
| Powerline Extra Symbols | `upstream-src/src/glyphs/powerline-extra/` | MIT | PowerlineExtraSymbols OTF plus README/LICENSE | Keep | Included by `--powerlineextra`. |
| Powerline Symbols | `upstream-src/src/glyphs/powerline-symbols/` | MIT-style free license | PowerlineSymbols OTF plus LICENSE | Keep | Included by `--powerline`. |
| IEC Power Symbols | `upstream-src/src/glyphs/Unicode_IEC_symbol_font.otf` | MIT, per Nerd Fonts `license-audit.md` | OTF glyph font | Keep | Included by `--powersymbols`. |
| Pomicons | `upstream-src/src/glyphs/pomicons/` | SIL OFL 1.1 | Pomicons OTF plus OFL license | Keep | Included by `--pomicons`. |
| Codicons | `upstream-src/src/glyphs/codicons/` | CC BY 4.0 | Codicons TTFs plus README/LICENSE | Keep | Included by `--codicons`. |

## Verification target

A compliant build must produce both package filenames and must not contain Font Logos codepoints `U+F300..U+F381`:

- `SymbolsNerdFont-Regular.ttf`
- `SymbolsNerdFontMono-Regular.ttf`
