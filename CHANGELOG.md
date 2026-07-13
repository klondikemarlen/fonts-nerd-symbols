# Changelog

All notable project-level changes are documented here.

This file follows [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/). Package upload metadata remains in `debian/changelog`; use that file as the authority for Debian/Ubuntu source package versions, distributions, and urgency.

## [Unreleased]

### Added

- Document project-level release history separately from Debian package upload metadata.

### Changed

- Clarify that Debian/Ubuntu package upload metadata remains in `debian/changelog`.
- Document the current `debian/latest` branch strategy and RFS `3.4.0+dfsg-2` snapshot.
- Improve source-preparation documentation for reviewability.

### Fixed

- Reject extra CLI arguments in build helper scripts instead of silently ignoring invocation typos.
- Fail clearly when `SOURCE_DATE_EPOCH` is missing during install timestamp normalization.
- Clean temporary changelog-prepend files on interrupted wrapper builds.

## [3.4.0+dfsg-1~ppa1] - 2026-07-09

### Changed

- Rebuilt Symbols Nerd Font from Nerd Fonts source inputs.
- Excluded Font Logos from the DFSG-targeted package.
- Published the DFSG-targeted PPA package for Ubuntu `resolute`.

## [3.4.0-3] - 2026-07-07

### Fixed

- Retouched installed files instead of changing the orig tarball.

## [3.4.0-2] - 2026-07-07

### Fixed

- Rebuilt with non-epoch mtimes for Launchpad publication.

## [3.4.0-1] - 2026-07-07

### Added

- Added the initial Symbols Nerd Font fontconfig fallback package.

[Unreleased]: https://github.com/klondikemarlen/fonts-nerd-symbols/compare/b3ec0f6ec1d34c69595be091311dd11babd1f28c...HEAD
[3.4.0+dfsg-1~ppa1]: https://ppa.launchpadcontent.net/klondikemarlen/fonts-nerd-symbols/ubuntu/pool/main/f/fonts-nerd-symbols/fonts-nerd-symbols_3.4.0+dfsg-1~ppa1.dsc
[3.4.0-3]: https://github.com/klondikemarlen/fonts-nerd-symbols/releases/tag/v3.4.0-3
[3.4.0-2]: https://github.com/klondikemarlen/fonts-nerd-symbols/releases/tag/v3.4.0-2
[3.4.0-1]: https://github.com/klondikemarlen/fonts-nerd-symbols/releases/tag/v3.4.0-1
