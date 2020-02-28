"""
"""

# Imports
from classifier.model_service import PEGI
from utils.eye import Eye
from detector.hand_detector import HILMI
from utils.sampler import get_sample_image
import cv2
from classifier.train.pickle_utility import get_pickle_object

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


# Global variables
eye = Eye()

# Regarding HILMI
weights_dir = "C:/Users/alaygut/Desktop/the-slate-prototype/" \
              "detector/weights/pegi.weights"
config_dir = "C:/Users/alaygut/Desktop/the-slate-prototype/pegi.cfg"

hilmi = HILMI(weights_dir, config_dir)

# Regarding PEGI
pickle_dir = "C:/Users/alaygut/Desktop/the-slate-prototype/" \
             "classifier/train/pickles"
model_path = "C:/Users/alaygut/Desktop/the-slate-prototype/" \
             "classifier/model_output/pegi.h5"

pegi = PEGI(model_path,
            get_pickle_object(f"{pickle_dir}/image_size.pickle"),
            get_pickle_object(f"{pickle_dir}/classes.pickle"),
            cv2.COLOR_BGR2GRAY)


def main():
    while True:
        image = eye.see()

        indexes, boxes, confidences = hilmi.detect(image)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                color = (0, 255, 0)
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                top_left = x, y
                bottom_right = x+w, y+h
                sample = get_sample_image(image, (top_left, bottom_right))
                result = pegi.predict(sample)
                print(result)

        cv2.imshow("The SLATE Demo", image)

        key = cv2.waitKey(1)

        if key == 27:
            break

    eye.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
