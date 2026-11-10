#!/usr/bin/python3
"""Check installed fallback behavior with competing private-use glyphs present."""

import os
import subprocess
import sys
import tempfile
import unittest

from PyQt6.QtGui import QFont, QGuiApplication, QRawFont, QTextLayout

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

    def test_missing_css_family_does_not_displace_later_text_family(self):
        for character in " Aa0!":
            with self.subTest(character=character):
                self.assertEqual(
                    matched_family(
                        f"Monaco,Consolas,Liberation Mono,monospace:"
                        f"charset={ord(character):x}"
                    ),
                    "Liberation Mono",
                )

    def test_firefox_family_lookup_does_not_substitute_icon_fonts(self):
        # Firefox uses a sentinel to distinguish family substitutions from
        # general fallbacks; anything before it becomes a CSS family candidate.
        families = subprocess.check_output(
            [
                "fc-pattern", "--config", "--format=%{family}",
                r"Monaco,\-moz-sentinel",
            ],
            text=True,
        ).split(",")
        substitutions = families[:families.index("-moz-sentinel")]
        for family in (
            "Symbols Nerd Font", "FontAwesome",
            "Material Design Icons version 6", "Material Design Icons version 5",
        ):
            with self.subTest(family=family):
                self.assertNotIn(family, substitutions)

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

    def test_generic_monospace_text_keeps_its_default_family(self):
        default_family = matched_family("monospace")
        for codepoint in ("20", "30", "41", "61"):
            with self.subTest(codepoint=codepoint):
                self.assertEqual(
                    matched_family(f"monospace:charset={codepoint}"),
                    default_family,
                )

    def test_explicit_mono_symbols_family_uses_companion_icons(self):
        self.assertEqual(
            matched_family("Symbols Nerd Font Mono:charset=f120"),
            "FontAwesome",
        )

    def test_unrelated_language_fallback_remains_available(self):
        self.assertEqual(matched_family("Hack:charset=ac00"), "UnDotum")

def laid_out_families(font, text):
    layout = QTextLayout(text, font)
    layout.beginLayout()
    line = layout.createLine()
    line.setLineWidth(1000)
    layout.endLayout()
    return [run.rawFont().familyName() for run in layout.glyphRuns()]

class QtFallbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QGuiApplication([])

    def test_qt_uses_font_awesome_for_reported_icons(self):
        font = QFont("Hack")
        font.setStyleHint(QFont.StyleHint.Monospace)
        for character in ("\uf120", "\uf07b", "\uf09b", "\uf17c"):
            with self.subTest(codepoint=hex(ord(character))):
                self.assertEqual(laid_out_families(font, character), ["FontAwesome"])

    def test_qt_preserves_generic_monospace_letters_digits_and_spaces(self):
        font = QFont("monospace")
        font.setStyleHint(QFont.StyleHint.Monospace)
        default_family = QRawFont.fromFont(font).familyName()
        for character in ("a", "0", " "):
            with self.subTest(character=character):
                self.assertEqual(
                    laid_out_families(font, character),
                    [default_family],
                )

if __name__ == "__main__":
    # Exercise system package configuration, not the invoking user's overrides.
    with tempfile.TemporaryDirectory() as home:
        runtime = os.path.join(home, "runtime")
        os.mkdir(runtime, mode=0o700)
        os.environ.update(
            HOME=home,
            XDG_CONFIG_HOME=home,
            XDG_CACHE_HOME=home,
            XDG_RUNTIME_DIR=runtime,
            QT_QPA_PLATFORM="offscreen",
            LC_ALL="C.UTF-8",
        )
        os.environ.pop("FONTCONFIG_FILE", None)
        os.environ.pop("FONTCONFIG_PATH", None)
        unittest.main(
            testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2),
        )
