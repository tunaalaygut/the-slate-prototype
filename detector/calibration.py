#!/usr/bin/env python

"""
calibration.py: Module that, given a list of sample images,
calculates the low and high thresholds that pixels need to fall in between
in order to be similar to the given sample images.
"""

# Imports
import cv2
import numpy as np

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"

# Global variables
# Experimental default values.
low_threshold = np.array([0, 133, 77], dtype="uint8")
high_threshold = np.array([235, 173, 127], dtype="uint8")
OFFSET_LOW = 20
OFFSET_HIGH = 20


def get_thresholds(sample_images=None, offset_low=OFFSET_LOW,
                   offset_high=OFFSET_HIGH, color_space=cv2.COLOR_BGR2YCrCb):
    """
    Returns the high and low thresholds that can be used to segment skin tone.

    Args:
        sample_images:
        offset_low:
        offset_high:
        color_space:

    Returns:
        Low and high thresholds calculated using sample images are returned as
        a tuple.
    """
    if sample_images:
        calculate_thresholds(sample_images, offset_low, offset_high,
                             color_space)
        # Print some information regarding the calculation results
        print("With offsets\n------------------")
        print("offsetLow:\t" + str(offset_low))
        print("offsetHigh:\t" + str(offset_high))
        print("\nThresholds are calculated as\n-----------------------------")
        print("LOW_THRESHOLD:\t" + str(low_threshold))
        print("HIGH_THRESHOLD:\t" + str(high_threshold))
    else:
        print("Default threshold values are returned.")
    return low_threshold, high_threshold


# Calculates the thresholds based on the given sample images.
def calculate_thresholds(sample_images, offset_low, offset_high, color_space):
    global low_threshold, high_threshold

    low_threshold = calculate_threshold(sample_images, True, offset_low,
                                        color_space)
    high_threshold = calculate_threshold(sample_images, False, offset_high,
                                         color_space)


# Calculates a single threshold.
def calculate_threshold(sample_images, is_low: bool, offset, color_space):
    first_channels = []
    second_channels = []
    third_channels = []

    for image in sample_images:
        image = cv2.cvtColor(image, color_space)
        # Mean value of each channel in the image.
        mean_channels = cv2.mean(image)
        first_channels.append(mean_channels[0])
        second_channels.append(mean_channels[1])
        third_channels.append(mean_channels[2])

    if is_low:	 # Low threshold is being calculated.
        return np.array([fit(first_channels, offset, False),
                         fit(second_channels, offset, False),
                         fit(third_channels, offset, False)], dtype="uint8")

    # High threshold is being calculated.
    return np.array([fit(first_channels, offset, True),
                     fit(second_channels, offset, True),
                     fit(third_channels, offset, True)], dtype="uint8")


# Fits the result of threshold calculations between 0 and 255.
def fit(a, offset, is_addition):
    if not is_addition:
        offset = -1 * offset
        func = min
    else:
        func = max

    return get_uint8(func(a) + offset)


# Takes a number, fits it to 8 bit.
def get_uint8(number):
    if number < 0:
        return 0
    if number > 255:
        return 255
    return number


def main():
    print("Excuse me?")


if __name__ == "__main__":
    main()

