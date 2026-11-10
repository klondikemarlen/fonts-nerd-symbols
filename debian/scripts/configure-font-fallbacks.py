#!/usr/bin/python3
"""Append Debian icon fallbacks after the complete requested family list."""

import sys
import xml.etree.ElementTree as ET

source, destination = sys.argv[1:]
tree = ET.parse(source)
root = tree.getroot()

# Handle explicit symbol requests before generic rules can introduce them weakly.
for family in ("Symbols Nerd Font", "Symbols Nerd Font Mono"):
    alias = ET.Element("alias")
    root.insert(0, alias)
    ET.SubElement(alias, "family").text = family

for alias in root.findall("alias"):
    family = alias.findtext("family")
    match = ET.SubElement(root, "match", target="pattern")
    test = ET.SubElement(match, "test", name="family", compare="eq")
    ET.SubElement(test, "string").text = family

    # A fallback belongs after ALL requested families, not immediately after
    # one missing family (which Firefox can treat as a CSS font substitution).
    # append_last cannot inherit binding: "same" becomes weak in Fontconfig.
    # Named requests need strong icons; generic monospace must remain weak.
    fallbacks = ET.SubElement(
        match, "edit", name="family", mode="append_last",
        binding="weak" if family == "monospace" else "strong",
    )
    for preferred in alias.findall("prefer/family"):
        ET.SubElement(fallbacks, "string").text = preferred.text

    for family in (
        "FontAwesome",
        "Material Design Icons version 6",
        "Material Design Icons version 5",
    ):
        ET.SubElement(fallbacks, "string").text = family
    root.remove(alias)

ET.indent(tree, space="  ")
tree.write(destination, encoding="utf-8", xml_declaration=True)
