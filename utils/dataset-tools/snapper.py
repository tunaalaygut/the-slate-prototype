"""
snapper.py: This tool is used to snap images from the given webcam source,
saves it to the given path with the given filename. Images are numbered
consecutively starting from 0. Starting count can be given as a parameter.
"""

# Imports
import cv2
import os
import argparse
from utils.eye import Eye

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"

# Global variables
parser = argparse.ArgumentParser(description="")
parser.add_argument('-o', '--path', required=True,
                    help="Output path of the snapped images.")
parser.add_argument('-n', '--name', required=True,
                    help="Filename given to the snapped images.")
parser.add_argument('-c', '--count', type=int, default=0,
                    help="Starting count of the snapped images.")
parser.add_argument('-ext', '--extension', default="png",
                    help="Extension of the snapped images.")
parser.add_argument('-w', "--webcam", default=0, help="Webcam source.")
args = vars(parser.parse_args())

output_path = args["path"]
filename = args["name"]
count = args["count"]
extension = args["extension"]
eye = Eye(source=args["webcam"])

title = "Snapper by SLATE"


def main():
    global count

    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    while True:
        image = eye.see()
        cv2.imshow(title, image)
        key = cv2.waitKey(1)

        if key == 27:
            break
        if key == 32:
            temp_filename = f"{output_path}/{filename}_{count}.{extension}"
            cv2.imwrite(temp_filename, image)
            print(f"Image {temp_filename} is saved.")

            count += 1
    eye.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
