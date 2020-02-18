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
            print(filename)
            new_filename = filename.replace('.xml', '.txt')
            # new_file = open(f"{path}/{new_filename}", "wb")
            file_path = os.path.join(path, filename)
            file = md.parse(file_path)
            size = file.getElementsByTagName("size")
            dimensions = size[0].childNodes
            dimension_count = 0
            image_height = 0
            image_width = 0
            for dimension in dimensions:
                if dimension.nodeType == md.Node.ELEMENT_NODE:
                    if dimension_count == 0:  # width
                        image_width = int(dimension.firstChild.data)
                        print(f"Width is {image_width}")
                    elif dimension_count == 1:  # height
                        image_height = int(dimension.firstChild.data)
                    dimension_count += 1

            # bndbox short for bounding box.
            bndboxes = file.getElementsByTagName("bndbox")

            for bndbox in bndboxes:
                child_nodes = bndbox.childNodes
                child_count = 0
                annotation_str = "0 "
                for child_node in child_nodes:
                    if child_node.nodeType == md.Node.ELEMENT_NODE:
                        value = int(child_node.firstChild.data)

                        if child_count % 2 == 0:  # x component
                            print(f"{value} / {image_width}")
                            annotation_str += f" {value/image_width}"
                        else:  # y component
                            print(f"{value} / {image_height}")
                            annotation_str += f" {value/image_height}"
                        child_count += 1
                annotation_str += "\n"
                print(annotation_str)


if __name__ == "__main__":
    main()
