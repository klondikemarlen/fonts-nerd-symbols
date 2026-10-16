#!/usr/bin/python3
"""Add Debian companions without promoting generic font preferences."""

import sys
import xml.etree.ElementTree as ET

source, destination = sys.argv[1:]
tree = ET.parse(source)
root = tree.getroot()

for family in ("Symbols Nerd Font", "Symbols Nerd Font Mono"):
    alias = ET.SubElement(root, "alias")
    ET.SubElement(alias, "family").text = family

for alias in root.findall("alias"):
    # Explicit text families retain strong priority; generic monospace must not
    # promote icon fonts ahead of the user's weakly bound concrete preferences.
    if alias.findtext("family") == "monospace":
        alias.set("binding", "weak")
    else:
        alias.set("binding", "same")

    fallbacks = alias.find("prefer")
    if fallbacks is None:
        fallbacks = ET.SubElement(alias, "accept")
    else:
        fallbacks.tag = "accept"

    for family in (
        "FontAwesome",
        "Material Design Icons version 6",
        "Material Design Icons version 5",
    ):
        ET.SubElement(fallbacks, "family").text = family

ET.indent(tree, space="  ")
tree.write(destination, encoding="utf-8", xml_declaration=True)
