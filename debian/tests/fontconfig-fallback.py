#!/usr/bin/python3
"""Check installed fallback behavior with competing private-use glyphs present."""

import os
import subprocess
import sys
import tempfile
import unittest

def matched_family(pattern):
    return subprocess.check_output(
        ["fc-match", "--format=%{family[0]}", pattern],
        text=True,
    ).strip()

class FontconfigFallbackTests(unittest.TestCase):
    def test_reported_font_awesome_icons_override_unrelated_glyphs(self):
        for codepoint in ("f120", "f07b", "f09b", "f17c"):
            with self.subTest(codepoint=codepoint):
                self.assertEqual(
                    matched_family(f"Hack:charset={codepoint}"),
                    "FontAwesome",
                )

    def test_selected_text_font_is_preserved(self):
        self.assertEqual(matched_family("Hack:charset=20 30 41 61"), "Hack")

    def test_selected_font_keeps_its_own_powerline_glyph(self):
        self.assertEqual(matched_family("Hack:charset=e0a0"), "Hack")

    def test_bundled_icons_override_unrelated_glyphs(self):
        self.assertEqual(
            matched_family("Hack:charset=ea60"),
            "Symbols Nerd Font",
        )

    def test_material_design_uses_compatible_supplementary_codepoints(self):
        self.assertEqual(
            matched_family("Hack:charset=f0001"),
            "Material Design Icons version 6",
        )

    def test_generic_monospace_uses_companion_icons(self):
        self.assertEqual(matched_family("monospace:charset=f120"), "FontAwesome")

    def test_explicit_mono_symbols_family_uses_companion_icons(self):
        self.assertEqual(
            matched_family("Symbols Nerd Font Mono:charset=f120"),
            "FontAwesome",
        )

    def test_unrelated_language_fallback_remains_available(self):
        self.assertEqual(matched_family("Hack:charset=ac00"), "UnDotum")

if __name__ == "__main__":
    # Exercise system package configuration, not the invoking user's overrides.
    with tempfile.TemporaryDirectory() as home:
        os.environ.update(
            HOME=home,
            XDG_CONFIG_HOME=home,
            XDG_CACHE_HOME=home,
            LC_ALL="C.UTF-8",
        )
        os.environ.pop("FONTCONFIG_FILE", None)
        os.environ.pop("FONTCONFIG_PATH", None)
        unittest.main(
            testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2),
        )
