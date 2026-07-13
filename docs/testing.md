# Testing

Use repo-native `make` targets. Do not add Node/npm just to launch tests; this repository is Debian packaging, shell scripts, and documentation.

## Fast offline checks

```bash
make test
```

This runs `tests/test_repo.py` and checks:

- shell syntax for package helper scripts;
- build helper argument validation;
- `SOURCE_DATE_EPOCH` failure and success behavior in `debian/rules`;
- local Markdown links;
- Keep a Changelog heading/reference shape;
- Debian copyright/license metadata coverage;
- Font Logos exclusion documented in the DFSG audit.

## Prepared source license inventory

```bash
make prepare-test-source
make test-prepared-source
```

This prepares the DFSG source tree, then verifies the Nerd Fonts v3.4.0 source inventory keeps required upstream notice/license files and excludes both Font Logos artifacts:

- `src/glyphs/font-logos.ttf`
- `bin/scripts/lib/i_logos.sh`

The inventory is intentionally pinned. If upstream changes file layout or license files, the test should fail and force a new audit instead of silently passing.

## Package install and removal smoke test

```bash
make test-integration
```

This runs in a privileged disposable Debian `unstable` container because
`piuparts` must mount a temporary chroot. The script copies the repo to `/tmp`,
builds the DFSG package,
checks the built `.deb` contains both expected TTF filenames, verifies neither
TTF contains Font Logos codepoints `U+F300..U+F381`, installs the exact `.deb`
for the current `debian/changelog` version, verifies fontconfig can see
`Symbols Nerd Font`, purges the package, then runs `piuparts`.

The fontconfig smoke checks include:

```bash
fc-list | grep -i 'Symbols Nerd Font'
fc-match 'Symbols Nerd Font'
fc-match -s 'monospace:charset=e0a0' | grep -m1 -i 'Symbols Nerd Font'
```

## Reproducibility check

```bash
make test-repro
```

This runs `reprotest` in a disposable Debian `unstable` container with
`/dev/fuse`, `SYS_ADMIN`, and unconfined AppArmor access for the file-ordering
variation. It prepares
the DFSG source tree, rebuilds the binary package twice under varied build
conditions, and compares the resulting `.deb` artifacts.

Run this after changes touching font generation, `debian/rules`, source preparation, or build dependencies. The generated TTF contents must be deterministic; timestamp normalization alone is not enough.
