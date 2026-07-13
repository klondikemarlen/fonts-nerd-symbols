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

Generate the upstream `orig.tar.xz` from the Nerd Fonts v3.4.0 source inputs needed to rebuild Symbols Only:

```text
./debian/scripts/prepare-upstream 3.4.0
```

The orig tarball carries the sparse upstream source under `upstream-src/`, not generated font binaries and not the upstream prebuilt NerdFontsSymbolsOnly.zip font binaries. Keep upstream README/LICENSE/audit files in the orig tarball so reviewers can inspect provenance.

Keep the orig tarball reproducible across Debian revisions of the same upstream version. Launchpad and Debian reject changed contents for the same source version/orig tarball identity. If a package upload is broken, upload a higher Debian revision instead of mutating an existing source version.

## DFSG and provenance audit

The bundled Symbols Only font is rebuilt from audited source inputs. Track the included glyph sources, licenses, preferred modification forms, and the Font Logos exclusion in [DFSG glyph provenance audit](dfsg-audit.md).

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

## Branch strategy

Use `main` as the long-lived PPA/GitHub release branch. Keep it protected.

Use `debian/latest` as the Debian packaging branch once Debian sponsorship work
exists. It may carry Debian-specific state such as `unstable`, ITP closures,
and the Debian packaging email.

Do not mix PPA changelog history and Debian archive submission history on the
same branch unless that is an explicit maintenance decision.

## Project changelog

Keep human-readable release notes in `CHANGELOG.md` using Keep a Changelog
1.0.0 sections. Keep Debian/Ubuntu upload metadata in `debian/changelog`; it
remains the authority for package versions, distributions, urgency, and bug
closures.

## Feature change workflow

Repo feature work follows `agents/workflows/feature-workflow.md`.

## Debian build environment

Build Debian `unstable` source uploads in a Debian environment, not on an Ubuntu host. Ubuntu-local `lintian` may reject `Distribution: unstable`, and Ubuntu builds can add Ubuntu-specific build metadata. A Debian container, sbuild, pbuilder, or VM is sufficient for this package.

After building for mentors, verify:

```text
Build-Origin: Debian
Distribution: unstable
```

Sign the regenerated Debian-built artifacts, not stale artifacts from another host.

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
