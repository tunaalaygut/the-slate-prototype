#!/usr/bin/env python

"""
sampler.py: Module that takes an image and a position as input and
outputs a sample images (portion of the input image with the given
position).
"""

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


# returns a single portion of an image.
def get_sample_image(image, position):
    """
    Args:
        image: Image to extract a portion of.
        position: Top left and bottom right points of the area to use when
        extracting the portion.

    Returns:
        The portion of the image.
    """
    top_left_x = get_top_left(position)[0]
    top_left_y = get_top_left(position)[1]

    bottom_right_x = get_bottom_right(position)[0]
    bottom_right_y = get_bottom_right(position)[1]

    return image[
           top_left_y + 2: bottom_right_y - 2,
           top_left_x + 2: bottom_right_x - 2
           ]


# Takes a position and returns the top left corner.
def get_top_left(position):
    return position[0][0], position[0][1]


# Takes a position and returns the bottom right corner.
def get_bottom_right(position):
    return position[1][0], position[1][1]
