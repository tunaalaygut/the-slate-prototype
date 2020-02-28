"""
"""

# Imports
from detector.eye import Eye
from detector.hand_detector import HandDetector
from detector.sampler import get_sample_image
from classifier import model_service
from tensorflow import keras
import cv2
from classifier.pickle_utility import get_pickle_object

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


# Global variables
eye = Eye()
hand_detector = HandDetector("pegi.weights", "pegi.cfg")
model = keras.models.load_model("classifier/model_output/pegi.h5")
image_size = get_pickle_object("./classifier/pickles/image_size.pickle")
classes = get_pickle_object("./classifier/pickles/classes.pickle")


def main():
    while True:
        image = eye.see()

        indexes, boxes = hand_detector.detect(image)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                color = (0, 255, 0)
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                top_left = x, y
                bottom_right = x+w, y+h
                sample = get_sample_image(image, (top_left, bottom_right))
                result = model_service.get_formatted_prediction(model,
                                                                sample,
                                                                image_size,
                                                                classes,
                                                                cv2.
                                                                COLOR_BGR2GRAY)
                print(result)

        cv2.imshow("The SLATE Demo", image)

        key = cv2.waitKey(1)

        if key == 27:
            break

    eye.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
