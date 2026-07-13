#!/usr/bin/env python3
import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

SCRIPTS = [
    "debian/scripts/prepare-upstream",
    "debian/scripts/build-clean-symbols",
    "debian/scripts/build-dfsg-package",
    "debian/scripts/build-full-package",
    "tests/integration-debian.sh",
    "tests/reprotest-debian.sh",
]

PYTHON_SCRIPTS = [
    "tests/test_repo.py",
    "tests/check-built-fonts.py",
]

EXTRA_ARGUMENT_CHECKS = [
    (["debian/scripts/prepare-upstream", "3.4.0+dfsg", "dfsg", "extra"], 2),
    (["debian/scripts/build-clean-symbols", "--dfsg", "/tmp/in", "/tmp/out", "extra"], 2),
    (["debian/scripts/build-dfsg-package", "3.4.0+dfsg-1", "resolute", "extra"], 2),
    (["debian/scripts/build-full-package", "3.4.0", "3.4.0-4~full1", "resolute", "extra"], 2),
]

REQUIRED_LICENSES = {"MIT", "Apache-2.0", "CC-BY-4.0", "OFL-1.1"}
REQUIRED_COPYRIGHT_PATHS = {
    "upstream-src/LICENSE",
    "upstream-src/license-audit.md",
    "upstream-src/src/unpatched-fonts/NerdFontsSymbolsOnly/*",
    "upstream-src/src/glyphs/font-awesome/FontAwesome.otf",
    "upstream-src/src/glyphs/font-awesome/analyze",
    "upstream-src/src/glyphs/font-awesome/generate",
    "upstream-src/src/glyphs/font-awesome/mapping",
    "upstream-src/src/glyphs/font-awesome/remix",
    "upstream-src/src/glyphs/font-awesome/remix_mapping",
    "upstream-src/src/glyphs/font-awesome/README.md",
    "upstream-src/src/glyphs/font-awesome/LICENSE.txt",
    "upstream-src/src/glyphs/materialdesign/MaterialDesignIconsDesktop.ttf",
    "upstream-src/src/glyphs/materialdesign/MaterialDesignIconsDesktop_orig.ttf",
    "upstream-src/src/glyphs/materialdesign/materialdesignicons-webfont.ttf",
    "upstream-src/src/glyphs/materialdesign/README.md",
    "upstream-src/src/glyphs/materialdesign/LICENSE",
    "upstream-src/src/glyphs/codicons/*",
    "upstream-src/src/glyphs/octicons/*",
    "upstream-src/src/glyphs/pomicons/*",
    "upstream-src/src/glyphs/weather-icons/*",
    "upstream-src/src/glyphs/powerline-extra/*",
    "upstream-src/src/glyphs/powerline-symbols/*",
}

REQUIRED_COPYRIGHT_STANZAS = {
    "upstream-src/src/glyphs/font-awesome/FontAwesome.otf": "OFL-1.1",
    "upstream-src/src/glyphs/font-awesome/analyze": "MIT",
    "upstream-src/src/glyphs/font-awesome/generate": "MIT",
    "upstream-src/src/glyphs/font-awesome/mapping": "MIT",
    "upstream-src/src/glyphs/font-awesome/remix": "MIT",
    "upstream-src/src/glyphs/font-awesome/remix_mapping": "MIT",
    "upstream-src/src/glyphs/font-awesome/README.md": "MIT",
    "upstream-src/src/glyphs/font-awesome/LICENSE.txt": "OFL-1.1 and CC-BY-4.0 and MIT",
    "upstream-src/src/glyphs/materialdesign/MaterialDesignIconsDesktop.ttf": "Apache-2.0",
    "upstream-src/src/glyphs/materialdesign/MaterialDesignIconsDesktop_orig.ttf": "Apache-2.0",
    "upstream-src/src/glyphs/materialdesign/materialdesignicons-webfont.ttf": "Apache-2.0",
    "upstream-src/src/glyphs/materialdesign/README.md": "MIT",
    "upstream-src/src/glyphs/materialdesign/LICENSE": "Apache-2.0 and MIT",
}

# Nerd Fonts v3.4.0 Symbols Only source notice/license inventory retained in the
# DFSG orig source. If upstream changes this inventory, fail here and re-audit.
REQUIRED_PREPARED_NOTICE_FILES = {
    "LICENSE",
    "license-audit.md",
    "src/unpatched-fonts/NerdFontsSymbolsOnly/LICENSE",
    "src/unpatched-fonts/NerdFontsSymbolsOnly/README.md",
    "src/glyphs/codicons/LICENSE.txt",
    "src/glyphs/font-awesome/LICENSE.txt",
    "src/glyphs/materialdesign/LICENSE",
    "src/glyphs/octicons/LICENSE",
    "src/glyphs/pomicons/LICENSE",
    "src/glyphs/powerline-extra/LICENSE",
    "src/glyphs/powerline-symbols/LICENSE.txt",
    "src/glyphs/weather-icons/OFL.txt",
    "src/glyphs/weather-icons/OFL-FAQ.txt",
}

EXCLUDED_FONT_LOGOS_FILES = {
    "src/glyphs/font-logos.ttf",
    "bin/scripts/lib/i_logos.sh",
}


def run(cmd, *, expect=0, env=None):
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if proc.returncode != expect:
        sys.stdout.write(proc.stdout)
        raise AssertionError(f"{cmd} exited {proc.returncode}, expected {expect}")
    return proc.stdout


def copyright_paragraphs(text):
    for raw in re.split(r"\n\s*\n", text.strip()):
        files = []
        license_name = None
        current = None
        for line in raw.splitlines():
            if line.startswith("Files:"):
                current = "Files"
                files.extend(line.removeprefix("Files:").split())
            elif line.startswith("License:"):
                current = "License"
                license_name = line.removeprefix("License:").strip()
            elif line.startswith(" ") and current == "Files":
                files.extend(line.split())
            else:
                current = None
        if files and license_name:
            yield files, license_name


def assert_copyright_stanza(text, path, license_name):
    for files, paragraph_license in copyright_paragraphs(text):
        if path in files and paragraph_license == license_name:
            return
    raise AssertionError(f"missing DEP-5 stanza: {path} -> {license_name}")


def test_shell_syntax():
    for script in SCRIPTS:
        run(["bash", "-n", script])


def test_python_syntax():
    for script in PYTHON_SCRIPTS:
        path = ROOT / script
        compile(path.read_text(), str(path), "exec")


def test_helper_arity_checks():
    for cmd, expected in EXTRA_ARGUMENT_CHECKS:
        output = run(cmd, expect=expected)
        assert "usage:" in output, output


def test_source_date_epoch_guard_and_success_path():
    pkg_root = ROOT / "debian" / "fonts-nerd-symbols"
    probe_dir = pkg_root / "tmp-smoke"
    if pkg_root.exists():
        raise AssertionError(f"refusing to overwrite existing package staging tree: {pkg_root}")
    try:
        probe_dir.mkdir(parents=True)
        probe = probe_dir / "probe.txt"
        probe.write_text("probe\n")

        env = os.environ.copy()
        env.pop("SOURCE_DATE_EPOCH", None)
        output = run(["make", "-f", "debian/rules", "execute_after_dh_install"], expect=2, env=env)
        assert "SOURCE_DATE_EPOCH must be set by dpkg-buildpackage" in output, output

        env["SOURCE_DATE_EPOCH"] = "1234567890"
        run(["make", "-f", "debian/rules", "execute_after_dh_install"], env=env)
        assert int(probe.stat().st_mtime) == 1234567890
    finally:
        shutil.rmtree(pkg_root, ignore_errors=True)


def markdown_links():
    return list(ROOT.glob("*.md")) + list((ROOT / "docs").glob("*.md"))


def test_local_markdown_links():
    missing = []
    for md in markdown_links():
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", md.read_text()):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if path and not (md.parent / path).exists():
                missing.append(f"{md.relative_to(ROOT)} -> {target}")
    assert not missing, "\n".join(missing)


def test_keep_a_changelog_shape():
    changelog = (ROOT / "CHANGELOG.md").read_text()
    headings = re.findall(r"^## \[([^\]]+)\]", changelog, re.M)
    refs = set(re.findall(r"^\[([^\]]+)\]:\s+\S+", changelog, re.M))
    missing_refs = [heading for heading in headings if heading not in refs]
    assert not missing_refs, missing_refs
    assert "Keep a Changelog 1.0.0" in changelog
    assert "debian/changelog" in changelog
    assert "full-symbols build path" in changelog
    assert "one-command DFSG package helper" in changelog


def test_license_metadata_inventory():
    copyright_text = (ROOT / "debian" / "copyright").read_text()
    for license_name in REQUIRED_LICENSES:
        assert f"License: {license_name}" in copyright_text
    for path in REQUIRED_COPYRIGHT_PATHS:
        assert path in copyright_text
    for path, license_name in REQUIRED_COPYRIGHT_STANZAS.items():
        assert_copyright_stanza(copyright_text, path, license_name)
    assert "Font Logos" in copyright_text
    assert "unlicensed" in copyright_text.lower()

    audit_text = (ROOT / "docs" / "dfsg-audit.md").read_text()
    assert "Font Logos" in audit_text
    for excluded in EXCLUDED_FONT_LOGOS_FILES:
        assert excluded in audit_text


def test_prepared_source_inventory(path):
    source = pathlib.Path(path)
    assert source.is_dir(), f"prepared source not found: {source}"
    for notice in sorted(REQUIRED_PREPARED_NOTICE_FILES):
        assert (source / notice).is_file(), notice
    for excluded in sorted(EXCLUDED_FONT_LOGOS_FILES):
        assert not (source / excluded).exists(), excluded


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepared-source")
    args = parser.parse_args()

    test_shell_syntax()
    test_python_syntax()
    test_helper_arity_checks()
    test_source_date_epoch_guard_and_success_path()
    test_local_markdown_links()
    test_keep_a_changelog_shape()
    test_license_metadata_inventory()
    if args.prepared_source:
        test_prepared_source_inventory(args.prepared_source)
    print("PASS tests/test_repo.py")


if __name__ == "__main__":
    main()
