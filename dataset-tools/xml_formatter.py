"""
xml_formatter.py: This module takes a path where the .xml files of a labeled
dataset and a file that has the class names. It creates .txt files that are
compatible with YOLOv3 and saves them into the directory.
"""

"""
WARNING: This module was being developed in order to use xml files with YOLOv3,
as it turns out, labelImg has yolo format, so the development is stopped.
"""

# Imports
import argparse
import os
import xml.dom.minidom as md

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


# Global variables
parser = argparse.ArgumentParser(description="")
parser.add_argument('-x', '--xml', required=True,
                    help="Path to the xml file(s).")
args = vars(parser.parse_args())

path = args["xml"]


class Annotation:
    def __init__(self, class_idx, top_left, bottom_right):
        self.class_idx = class_idx
        self.x_max = top_left[0]
        self.y_max = top_left[1]
        self.x_min = bottom_right[0]
        self.y_min = bottom_right[1]

    def get_string(self):
        return f"{self.class_idx} {self.x_max} {self.y_max} " \
               f"{self.x_min} {self.y_min}"


def main():
    for filename in os.listdir(path):
        if filename.endswith(".xml"):
            new_filename = filename.replace('.xml', '.txt')
            # new_file = open(new_filename, "wb")
            file_path = os.path.join(path, filename)
            file = md.parse(file_path)
            # bndbox short for bounding box.
            bndboxes = file.getElementsByTagName("bndbox")

            for bndbox in bndboxes:
                child_nodes = bndbox.childNodes
                annotation_str = "0 "
                for child_node in child_nodes:
                    if child_node.nodeType == md.Node.ELEMENT_NODE:
                        annotation_str += f" {child_node.firstChild.data}"
                annotation_str += "\n"
                print(annotation_str)


if __name__ == "__main__":
    main()
