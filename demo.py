#!/usr/bin/env python
"""
demo.py: Module that, brings the modules inside the detector and
classifier packages to perform the intended functionality of 
the Slate project. This module is created to demonstrate the
capabilities of the project.

It includes two modes;

Prediction mode: Mode that uses the classifier model
to predict what gesture is being shown.

Data collection mode: Takes images from the webcam and
stores it to the specified path with the specified filename.
"""

# Imports
from detector import eye
from detector import calibration
from detector import skin_detector
from detector import drawing_utility
from detector import sampler
from detector import model_service
from detector import data_gatherer
from detector import position_provider
from classifier.pickle_loader import get_pickle_object

import cv2
import argparse
import numpy as np
from tensorflow import keras

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"

# Arguments to the program are defined below.
parser = argparse.ArgumentParser(description='')
# By default, program starts in prediction mode.
parser.add_argument('-m', '--mode', type=int, default=0,
                    help="mode of operation, 0: predict, 1: collect data")
# By default, program starts with calibration mode on.
parser.add_argument('-c', '--calibration', type=int, default=1,
                    help="skin calibration is on. (1 or 0)")
# By default program starts with 2 samples to take.
parser.add_argument('-s', '--samples', type=int, default=2,
                    help="number of samples to take")

# Data collection mode arguments
parser.add_argument('-o', '--outputpath',
                    help="output path for images")
parser.add_argument('-f', '--filename',
                    help="name for images")
parser.add_argument('-l', '--limit', type=int, default=9999,
                    help="limit the number of images that will be taken")
parser.add_argument('-n', '--imagecount', type=int, default=0,
                    help="start count of the images")
args = vars(parser.parse_args())

# Global Variables
main_loop = True

op_mode = args["mode"]

if op_mode == 1 and (args["outputpath"] is None or args["filename"] is None):
    parser.error("--mode 1 requires --outputpath and --filename.")

calibration_mode = bool(args["calibration"])
calibrated = not calibration_mode
samples_to_take = int(args["samples"])

low_threshold = np.array([0, 133, 77], dtype="uint8")
high_threshold = np.array([235, 173, 127], dtype="uint8")

window_title = "P.E.G.I. & Skin Detection Demo"

image_size = get_pickle_object("./classifier/pickles/image_size.pickle")
classes = get_pickle_object("./classifier/pickles/classes.pickle")

model = keras.models.load_model("./classifier/model_output/pegi.h5")

data_gatherer = data_gatherer.DataGatherer(args["outputpath"],
                                           args["filename"],
                                           image_count=args["imagecount"],
                                           limit=args["limit"])

# Global variables of skin calibration
sample_positions = []

sampleAreaOnePosition = position_provider.get_top_left(eye.see(), scale=0.1)
sampleAreaTwoPosition = position_provider.get_top_right(eye.see(), scale=0.1)

print(eye.see().shape)

sample_positions.append(sampleAreaOnePosition)
sample_positions.append(sampleAreaTwoPosition)

samples_to_take = len(sample_positions)
samples_taken = 0

sample_images = []

pred_area_pos = position_provider.get_center(eye.see(), scale=0.6)


# Main function
def main():
    print("Welcome to P.E.G.I. & Skin Detection Demo\n"
          "-----------------------------------------\n")

    while main_loop:
        image = eye.see()
        final_image = []

        # Program is running with calibration mode on
        # and have not been calibrated yet.
        if calibration_mode and not calibrated:
            image_r = image.copy()  # Image to draw the rectangles on.
            # Draw the calibration rectangles on the image.
            image_r = drawing_utility.draw_rectangle(image_r,
                                                     sampleAreaOnePosition,
                                                     thickness=2)
            image_r = drawing_utility.draw_rectangle(image_r,
                                                     sampleAreaTwoPosition,
                                                     thickness=2,
                                                     color=(0, 0, 255))
            final_image = image_r

        # If calibration has been done.
        if calibrated:
            final_image = skin_detector.get_skin_image(image, low_threshold,
                                                       high_threshold)
            image = final_image  # Because it will be sent to the handle_key.

            final_image = \
                drawing_utility.draw_rectangle(final_image,
                                               pred_area_pos,
                                               thickness=2,
                                               color=(255, 255, 0))
            # Program is in prediction mode.
            if op_mode == 0:
                prediction_image = \
                    sampler.get_sample_image(final_image,
                                             pred_area_pos)
                prediction_text, percentage = \
                    model_service.get_prediction(model,
                                                 prediction_image,
                                                 image_size,
                                                 classes,
                                                 cv2.COLOR_BGR2GRAY)

                if percentage > 90:
                    final_image = \
                        drawing_utility.draw_text(final_image,
                                                  "It is {} {}".
                                                  format(prediction_text,
                                                         round(percentage, 2)),
                                                  (pred_area_pos[0][0],
                                                   pred_area_pos[1][1] + 23),
                                                  scale=0.8,
                                                  color=(0, 0, 255),
                                                  thickness=1)
        cv2.imshow(window_title, final_image)

        key = cv2.waitKey(1)

        handle_key(key, image)

    cv2.destroyAllWindows()


def handle_key(key, image):
    global calibrated, low_threshold, high_threshold, samples_taken, main_loop

    # ESC key is pressed.
    if key == 27:
        main_loop = False

    # Space key is pressed in data collection mode.
    if key == 32 and op_mode == 1 and calibrated:
        data_image = sampler.get_sample_image(image, pred_area_pos)
        data_gatherer.save_image(data_image)

    # If program is being run with calibration mode
    # and calibration has not been made yet. 's' key is pressed.
    if key == 115 and calibration_mode and not calibrated:
        if samples_taken < samples_to_take:
            sample_image = sampler.\
                get_sample_image(image, sample_positions[samples_taken])
            sample_images.append(sample_image)
            samples_taken += 1
            print("Sample {} is taken.".format(samples_taken))

            if samples_taken == samples_to_take:
                print("\nPress s to start skin detection...\n")
        else:
            (low_threshold, high_threshold) = \
                calibration.get_thresholds(sample_images)
            # Works better this way.  WHY????  YCrCb study might explain.
            low_threshold[0] = 0
            high_threshold[0] = 235
            calibrated = True


if __name__ == "__main__":
    main()
