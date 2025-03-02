import os
import xml.etree.ElementTree as ET

# Define your class names
class_names = ["DWS-01", "DWS-02", "DWS-03", "DWS-04", "DWS-10", "DWS-11", "DWS-12", "DWS-13",
    "DWS-14", "DWS-17", "DWS-18", "DWS-19", "DWS-21", "DWS-25", "DWS-26", "DWS-32",
    "DWS-33", "DWS-35", "DWS-40", "DWS-41", "MNS-01", "MNS-06", "MNS-07", "MNS-09",
    "OSD-01", "OSD-02", "OSD-03", "OSD-04", "OSD-06", "OSD-07", "OSD-16", "OSD-17",
    "OSD-26", "PHS-01", "PHS-02", "PHS-03", "PHS-04", "PHS-09", "PHS-23", "PHS-24",
    "PRS-01", "RSS-02", "SLS-100", "SLS-15", "SLS-40", "SLS-50", "SLS-60", "SLS-70",
    "SLS-80", "APR-09", "APR-10", "APR-11", "APR-12", "APR-14", "TLS-C", "TLS-E",
    "TLS-G", "TLS-R", "TLS-Y"]  # Add all your classes

# Paths
input_dir = "train/train/"  # Folder containing XML annotation files
output_dir = "train/labels/"  # Folder to save YOLO formatted labels
os.makedirs(output_dir, exist_ok=True)

for xml_file in os.listdir(input_dir):
    if xml_file.endswith(".xml"):
        tree = ET.parse(os.path.join(input_dir, xml_file))
        root = tree.getroot()

        # Extract image size
        image_width = int(root.find("size/width").text)
        image_height = int(root.find("size/height").text)

        # Output YOLO label file
        yolo_label_file = os.path.join(output_dir, xml_file.replace(".xml", ".txt"))

        with open(yolo_label_file, "w") as f:
            for obj in root.findall("object"):
                class_name = obj.find("name").text
                if class_name not in class_names:
                    continue  # Ignore classes not in class_names
                
                class_id = class_names.index(class_name)  # Get class index
                bbox = obj.find("bndbox")
                xmin = int(bbox.find("xmin").text)
                ymin = int(bbox.find("ymin").text)
                xmax = int(bbox.find("xmax").text)
                ymax = int(bbox.find("ymax").text)

                # Convert to YOLO format (normalized values)
                x_center = (xmin + xmax) / 2 / image_width
                y_center = (ymin + ymax) / 2 / image_height
                width = (xmax - xmin) / image_width
                height = (ymax - ymin) / image_height

                # Write to YOLO format file
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

print("Conversion complete! YOLO format annotations saved in 'labels/' folder.")
