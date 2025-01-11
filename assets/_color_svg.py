import os
from xml.etree import ElementTree as ET

svg_directory = "."
output_directory = "."
new_fill_color = "#328fa8"

os.makedirs(output_directory, exist_ok=True)

for file_name in os.listdir(svg_directory):
    if file_name.endswith(".svg"):
        file_path = os.path.join(svg_directory, file_name)

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            namespace = "{http://www.w3.org/2000/svg}"

            for element in root.findall(f".//{namespace}path"):
                element.set("fill", new_fill_color)
            if "fill" in root.attrib:
                root.set("fill", new_fill_color)

            output_path = os.path.join(output_directory, file_name)
            tree.write(output_path)
            print(f'<img src="assets/{file_name}" class="social-icon">')
        except Exception as e:
            print(f"Failed to update {file_name}: {e}")
