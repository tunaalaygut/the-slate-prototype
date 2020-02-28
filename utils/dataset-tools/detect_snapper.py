"""
detect_snapper.py: This module uses hand_detection capabilities of the project
and only snaps images of the hands.
"""

# Imports
from utils.eye import Eye
from detector.hand_detector import HandDetector
from utils import sampler
import cv2
import argparse
import os

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
hand_detector = HandDetector("../pegi.weights", "../pegi.cfg")


def main():
    global count

    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    while True:
        frame = eye.see()
        indexes, boxes = hand_detector.detect(frame)
        samples = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                top_left = x, y
                bottom_right = x+w, y+h
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                samples.append(sampler
                               .get_sample_image(frame,
                                                 (top_left, bottom_right)))

        cv2.imshow("Detection", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
        if key == 32:
            for sample in samples:
                temp_filename = f"{output_path}/{filename}_{count}.{extension}"
                print(f"Image {temp_filename} is saved.")
                cv2.imwrite(temp_filename, sample)
                count += 1

    eye.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
