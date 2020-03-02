"""
"""

# Imports
from classifier.model_service import PEGI
from utils.eye import Eye
from detector.hand_detector import HILMI
from utils.sampler import get_sample_image
import cv2
from classifier.train.pickle_utility import get_pickle_object
from imutils.video import FPS

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


# Global variables
eye = Eye()

# Regarding PEGI
pickle_dir = "C:/Users/alaygut/Desktop/the-slate-prototype/" \
             "classifier/train/pickles"
model_path = "C:/Users/alaygut/Desktop/the-slate-prototype/" \
             "classifier/model_output/pegi.h5"

pegi = PEGI(model_path,
            get_pickle_object(f"{pickle_dir}/image_size.pickle"),
            get_pickle_object(f"{pickle_dir}/classes.pickle"))

# Regarding HILMI
weights_dir = "C:/Users/alaygut/Desktop/the-slate-prototype/" \
              "detector/weights/hilmi.weights"
config_dir = "C:/Users/alaygut/Desktop/the-slate-prototype/hilmi-test.cfg"

hilmi = HILMI(weights_dir, config_dir, use_gpu=True)


def main():
    fps = FPS().start()
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
                result = pegi.classify(sample)
                print(result)

        cv2.imshow("The SLATE Demo", image)
        fps.update()
        key = cv2.waitKey(1)

        if key == 27:
            break

    fps.stop()
    eye.release()
    cv2.destroyAllWindows()
    print(f"FPS: {fps.fps()}")


if __name__ == "__main__":
    main()
