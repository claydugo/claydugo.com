import os
from xml.etree import ElementTree as ET

# Icons are colored by `.social-icon { fill: currentcolor }` in stylesheet.css;
# currentColor here keeps the files in sync with --primary-color instead of
# baking in a hex value that goes stale when the palette changes.
new_fill_color = "currentColor"
svg_directory = "."

# Without a registered default namespace, ElementTree serializes <ns0:svg>,
# which HTML parsers can't render when the file is inlined.
ET.register_namespace("", "http://www.w3.org/2000/svg")


def recolor_style(style):
    declarations = []
    for declaration in style.split(";"):
        name, _, value = declaration.partition(":")
        if name.strip() == "fill" and value.strip() != "none":
            declaration = f"fill:{new_fill_color}"
        if declaration.strip():
            declarations.append(declaration.strip())
    return ";".join(declarations)


for file_name in sorted(os.listdir(svg_directory)):
    if not file_name.endswith(".svg"):
        continue
    file_path = os.path.join(svg_directory, file_name)
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # Fills can live on any shape or group, as an attribute or inside
        # style=""; fill="none" is preserved (it cuts holes/disables shapes).
        for element in root.iter():
            if element.get("fill") not in (None, "none"):
                element.set("fill", new_fill_color)
            style = element.get("style")
            if style and "fill" in style:
                element.set("style", recolor_style(style))
        root.set("fill", new_fill_color)
        tree.write(file_path)
        print(f'{file_name}: fill set to {new_fill_color} (inline as <svg class="social-icon">)')
    except ET.ParseError as e:
        print(f"Failed to update {file_name}: {e}")
