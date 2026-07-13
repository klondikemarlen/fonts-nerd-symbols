#!/usr/bin/env python3
import argparse
import pathlib
import subprocess
import tempfile

from fontTools.ttLib import TTFont

FONT_DIR = pathlib.Path("usr/share/fonts/truetype/nerd-fonts-symbols")
EXPECTED_TTFS = [
    FONT_DIR / "SymbolsNerdFont-Regular.ttf",
    FONT_DIR / "SymbolsNerdFontMono-Regular.ttf",
]
FORBIDDEN_FONT_LOGOS = range(0xF300, 0xF382)


def cmap_codepoints(ttf_path):
    font = TTFont(ttf_path)
    try:
        codepoints = set()
        for table in font["cmap"].tables:
            codepoints.update(table.cmap.keys())
        return codepoints
    finally:
        font.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package_deb")
    args = parser.parse_args()

    package_deb = pathlib.Path(args.package_deb)
    if not package_deb.is_file():
        raise SystemExit(f"package not found: {package_deb}")

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        subprocess.run(["dpkg-deb", "-x", str(package_deb), str(root)], check=True)
        for relative in EXPECTED_TTFS:
            ttf = root / relative
            if not ttf.is_file():
                raise SystemExit(f"missing expected font: {relative}")
            present = cmap_codepoints(ttf)
            forbidden = sorted(cp for cp in FORBIDDEN_FONT_LOGOS if cp in present)
            if forbidden:
                formatted = ", ".join(f"U+{cp:04X}" for cp in forbidden)
                raise SystemExit(f"{relative} contains Font Logos codepoints: {formatted}")
    print("PASS tests/check-built-fonts.py")


if __name__ == "__main__":
    main()
