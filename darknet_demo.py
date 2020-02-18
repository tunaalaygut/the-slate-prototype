"""
"""

# Imports
import cv2
from detector.eye import Eye
from detector.hand_detector import HandDetector

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"

# Global variables
eye = Eye()
hand_detector = HandDetector("pegi.weights", "pegi.cfg")


def main():
    while True:
        img = eye.see()
        indexes, boxes = hand_detector.detect(img)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                color = (0, 255, 0)
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

        cv2.imshow("Result", img)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
