# Debian-first package submission

Use this path when you want `fonts-nerd-symbols` to become an official Debian package first, then flow into Ubuntu by normal sync.

Use `debian/latest` as the long-lived Debian packaging branch. Keep PPA/GitHub release work on `main` so Ubuntu series changelog targets such as `resolute` do not accidentally switch to `unstable`.

## Flow

1. File an ITP bug for `fonts-nerd-symbols`.
2. Create a linked issue and draft pull request against `debian/latest`.
3. Complete the [pull request review and QA](build.md#pull-request-review-and-qa) before merging.
4. Update `debian/changelog` to close it: `Closes: #NNNNNN`.
5. Set the changelog distribution to `unstable` on the Debian packaging branch.
6. Build a signed source package with `debuild -S -sa` for a new upstream orig tarball, or `debuild -S -sd` for later Debian revisions of the same upstream version.
7. Run `lintian` on the source `.changes` and `.dsc`, then a clean `sbuild` build.
8. Sign the source artifacts with the registered OpenPGP key.
9. Upload to mentors.debian.net.
10. File an RFS bug against `sponsorship-requests` by sending the mentors RFS template to `submit@bugs.debian.org`.
11. Pass Debian NEW review.
12. After archive acceptance, complete [Debian bug closure](#debian-bug-closure) for every fixed bug.
13. Ubuntu can later sync the package from Debian.

## File the ITP

Install and configure `reportbug`:

```bash
sudo apt install reportbug
reportbug --configure
```

For Ubuntu hosts, make sure `reportbug` targets Debian, not Ubuntu:

```bash
reportbug -B debian wnpp
```

If `reportbug` starts paging through thousands of existing WNPP bugs, quit and rerun without the duplicate-query browser:

```bash
reportbug -B debian --no-query-bts wnpp
```

Choose `ITP - Intent To Package`.

Suggested metadata:

```text
Package: fonts-nerd-symbols
Short description: Nerd Fonts symbols fallback for fontconfig
License: DFSG-free rebuilt Symbols Nerd Font, excluding Font Logos
Upstream: https://github.com/ryanoasis/nerd-fonts
Packaging: https://salsa.debian.org/klondikemarlen/fonts-nerd-symbols
```

Suggested long description:

```text
Installs Symbols Nerd Font and fontconfig aliases so existing terminal fonts
such as Ubuntu Sans Mono can render Nerd Font icon glyphs without switching
the whole terminal font.
```

Mention these specifics in the bug or sponsor notes:

- this is a fonts package, not an application;
- the package rebuilds the Nerd Fonts Symbols Only assets from upstream source inputs;
- Font Logos is excluded because upstream marks it unlicensed and Debian notes flag logo glyphs as likely non-distributable;
- the completed [DFSG/provenance audit](dfsg-audit.md) records every included glyph source, license, preferred form for modification, and the Font Logos exclusion;
- normal text continues to render with the user's selected monospace font;
- `Symbols Nerd Font` is only a fallback for missing icon/private-use glyphs;
- the intended install paths are under `/usr/share/fonts/truetype/nerd-fonts-symbols/`, `/usr/share/fontconfig/conf.avail/`, and `/etc/fonts/conf.d/`.

## Changelog for Debian

Current Debian tracker snapshot (2026-07-13):

```text
ITP: #1141696
RFS: #1141699
Current mentors upload: fonts-nerd-symbols_3.4.0+dfsg-2
Mentors package: https://mentors.debian.net/package/fonts-nerd-symbols/
```

For a future first upload of a new package, after the ITP exists, update
`debian/changelog` on the Debian branch:

```text
fonts-nerd-symbols (NEXT_VERSION) unstable; urgency=medium

  * Initial release. (Closes: #NNNNNN)

 -- Marlen Brunner <klondikemarlen+debian@gmail.com>  DATE
```

For later review revisions, keep the ITP closure in the latest uploaded
changelog stanza or close the ITP manually after archive acceptance. Use the
public Debian packaging email you used for the ITP. Do not change the PPA branch
from `resolute` to `unstable`; keep Debian submission work on `debian/latest`.

## Debian bug closure

For every Debian bug-fix release, follow the official [Debian BTS procedure for closing bug reports](https://www.debian.org/Bugs/Developer#closing). A merge, GitHub release, Mentors upload, or SMTP acceptance is not confirmed Debian bug closure.

1. **Before upload:** list every bug fixed since the last version accepted into Debian, including fixes in superseded, unpublished revisions. Check that each number appears in the generated source `.changes` file's `Closes` field, not merely somewhere in `debian/changelog`. If an earlier stanza was omitted, carry the relevant closure into the current stanza or include the full changelog range since the last accepted version when generating `.changes`; rebuild and re-sign the upload, then check the field again. Do not edit a signed `.changes` file.
2. **Prove the shipped fix:** verify archive acceptance and the exact accepted version on the [Debian package tracker](https://tracker.debian.org/pkg/fonts-nerd-symbols). Exercise the reported failure against the released artifact in isolation and preserve the affected-versus-fixed evidence. If testing generated configuration separately, establish that the archived binary ships identical configuration. Do not close an unproven fix or use a newer local revision as proof of an older archived version.
3. **Check automatic closure:** read each public bug record after acceptance. Confirm both its closed status and the fixed version. A `Closes` entry in an unpublished revision can be missed by the eventual upload; do not assume archive acceptance closed every intended bug.
4. **Recover a missed closure:** once the fix is proven and in the archive, the maintainer sends a concise explanation to `NNNNNN-done@bugs.debian.org`, using the version that actually entered Debian. For this source package, use the following body, replacing every placeholder:

   ```text
   Source: fonts-nerd-symbols
   Source-Version: ACCEPTED_VERSION

   This is fixed in ACCEPTED_VERSION, now available in Debian.
   EXPLAIN_THE_FIX_AND_THE_OBSERVED_BEHAVIOR_CHECK.
   LINK_TO_ARCHIVE_ACCEPTANCE_AND_RELEVANT_FIX_EVIDENCE.
   ```

   Ordinary mail to `NNNNNN@bugs.debian.org` does not close the bug. Do not rely on a `Control:` pseudo-header sent only to the `-done` address; it is unsupported there. Follow the official procedure above for other control operations.
5. **Confirm completion:** read back the public BTS record and verify the closed status and correct fixed version. Until processing is visible, report “closure submitted; confirmation pending,” retain the message ID, and do not blindly resend. For a release-critical bug, also check the package tracker's autoremoval status after its next refresh; closure and removal of that warning are separate observations. Do not claim the removal is cancelled until the tracker confirms it.

Keep a recurring sponsorship tracker open; record the individual release's archive acceptance and bug-closure outcome without closing the ongoing tracker.

## Build source for review

Build Debian uploads in Debian, not Ubuntu. Ubuntu's `lintian` can reject `Distribution: unstable`, and Ubuntu-built source metadata can include Ubuntu-specific build context.

Use `sbuild` with `sbuild-schroot` for the clean Debian build. Configure an `unstable` chroot once:

```bash
sudo sbuild-adduser "$USER"
sudo sbuild-createchroot unstable /srv/chroot/unstable-amd64-sbuild http://deb.debian.org/debian
```

Start a new shell after adding the group. Prepare, build, and lint the source package:

```bash
UPSTREAM_VERSION="$(dpkg-parsechangelog -S Version | sed 's/-[^-]*$//')"
SOURCE_VERSION="$(dpkg-parsechangelog -S Version)"
./debian/scripts/prepare-upstream "$UPSTREAM_VERSION"
(
  cd "build/fonts-nerd-symbols-$UPSTREAM_VERSION"
  debuild -S -sa -us -uc
  lintian --profile debian "../fonts-nerd-symbols_${SOURCE_VERSION}_source.changes" "../fonts-nerd-symbols_${SOURCE_VERSION}.dsc"
)
sbuild --chroot-mode=schroot --dist=unstable --arch=amd64 "build/fonts-nerd-symbols_${SOURCE_VERSION}.dsc"
```

Use `-sa` for the first Debian upload of a new upstream orig tarball. Use `-sd` only for later Debian revisions of the same upstream version after the orig tarball is already in the target archive.

Sign the regenerated source upload with the registered key:

```bash
debsign -kFULL_FINGERPRINT build/fonts-nerd-symbols_${SOURCE_VERSION}_source.changes
```

The `.dsc`, `.buildinfo`, and `_source.changes` files should begin with a PGP signed message header after signing.

## Upload to mentors

Register the same public OpenPGP key in your mentors.debian.net account. Export only the public key:

```bash
gpg --export --export-options export-minimal --armor FULL_FINGERPRINT
```

Do not export or upload secret keys.

Upload the signed source package:

```bash
dput mentors build/fonts-nerd-symbols_${SOURCE_VERSION}_source.changes
```

If the `mentors` dput profile is missing, use the mentors.debian.net web upload or add the mentors upload profile from their maintainer instructions.

After mentors accepts the upload, it sends the public package page, `.dsc` URL, and an RFS helper URL. Use those links in the sponsorship request instead of guessing paths.

## Submit for sponsorship

After mentors accepts the upload and shows a package page, file one RFS bug
against `sponsorship-requests` if none exists. If an RFS already exists, send a
follow-up to `NNNNNN@bugs.debian.org` with the new `.dsc` URL, `dget -x`
command, and latest `debian/changelog` stanza.

For the current Debian submission of this package:

```text
ITP: #1141696
RFS: #1141699
Mentors upload: fonts-nerd-symbols_3.4.0+dfsg-2
DSC: https://mentors.debian.net/debian/pool/main/f/fonts-nerd-symbols/fonts-nerd-symbols_3.4.0+dfsg-2.dsc
Debian packaging branch: https://salsa.debian.org/klondikemarlen/fonts-nerd-symbols/-/tree/debian/latest
```

Typical RFS subject:

```text
RFS: fonts-nerd-symbols/3.4.0+dfsg-2 [ITP] -- Nerd Fonts symbols fallback for fontconfig
```

Include the ITP bug number, mentors package URL, source package URL, lintian result, a short note that this is a fonts/fontconfig fallback package, and the completed DFSG/provenance audit.

Sponsor review will focus on licensing, source/orig tarball construction, preferred form for modification for bundled glyph sources, Debian font paths, fontconfig behavior, lintian output, and whether generated/binary font assets are handled according to Debian policy.
