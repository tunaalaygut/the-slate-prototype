#!/usr/bin/env python

"""
skin_detector.py: Module that, given an image and two thresholds
(low and high), produces an image that is showing all the skin pixels and
masking all the non-skin pixels.
"""

# Imports
import cv2

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


# Returns the skin image.
def get_skin_image(image, low_threshold, high_threshold,
                   color_space=cv2.COLOR_BGR2YCrCb):
    """
    Function that finds and masks the areas that are outside of two given
    (high and low) threshold values.

    Args:
        image: Image to apply the thresholds to.
        low_threshold: Lower limit of channel values.
        high_threshold: Upper limit of channel values.
        color_space: Color space to convert the image.

    Returns:
        The image with the areas outside the threshold values masked out.
    """
    skin_image = apply_threshold(image, low_threshold, high_threshold,
                                 color_space)
    return skin_image


# Function that applies the actual threshold. Leaves out the areas of the image
# that are not inside the specified thresholds.
def apply_threshold(image, low_threshold, high_threshold, color_space):
    threshold_image = cv2.cvtColor(image, color_space)

    mask = cv2.inRange(threshold_image, low_threshold, high_threshold)
    mask = morphological_operations(mask)

    return cv2.bitwise_and(image, image, mask=mask)


# Morphological operations, they need to inputs;
# one the image to apply the operation to and
# second the kernel or a structuring element which decides
# the nature of the operation.
def morphological_operations(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))

    image = cv2.erode(image, kernel, iterations=2)
    image = cv2.dilate(image, kernel, iterations=2)
    image = cv2.GaussianBlur(image, (3, 3), 0)

    return image


def main():
    print("Excuse me?")


if __name__ == "__main__":
    main()
