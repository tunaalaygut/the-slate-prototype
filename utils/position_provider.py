#!/usr/bin/env python

"""
position_provider.py: Module that, provides positions to be used when
drawing rectangles in the form of a tuple (topLeft, bottomRight).
Positions are calculated based on the frame size. Difference between points is
based on the scale input.
"""

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


def get_top_left(image, scale=0.25, padding=25):
    """
    Args:
        image: Image that the rectangle will be drawn on top of.
        scale: Scale of the rectangle wrt the smaller side of the image.
        padding: Padding to be left on the top and left of the image.

    Returns:
        Returns the suitable position of a rectangle that can be drawn on the
        top left of the given image.
    """
    (height, width, _) = image.shape

    rectangle_size = get_rectangle_size(height, width, scale)

    top_left = (padding, padding)
    bottom_right = (padding + rectangle_size, padding + rectangle_size)

    return top_left, bottom_right


def get_top_right(image, scale=0.25, padding=25):
    """
    Args:
        image: Image that the rectangle will be drawn on top of.
        scale: Scale of the rectangle wrt the smaller side of the image.
        padding: Padding to be left on the top and left of the image.

    Returns:
        Returns the suitable position of a rectangle that can be drawn on the
        top right of the given image.
    """
    (height, width, _) = image.shape

    rectangle_size = get_rectangle_size(height, width, scale)

    top_left = (width - (padding + rectangle_size), padding)
    bottom_right = (width - padding, padding + rectangle_size)

    return top_left, bottom_right


def get_center(image, scale=0.25):
    """
    Args:
        image: Image that the rectangle will be drawn on top of.
        scale: Scale of the rectangle wrt the smaller side of the image.

    Returns:
        Returns the positions of the rectangle that can be drawn on the
        center of an image.
    """
    (height, width, _) = image.shape
    rectangle_size = get_rectangle_size(height, width, scale)

    center_x = int(width/2)
    center_y = int(height/2)

    top_left = (center_x - int(rectangle_size/2),
                center_y - int(rectangle_size/2))
    bottom_right = (center_x + int(rectangle_size/2),
                    center_y + int(rectangle_size/2))

    return top_left, bottom_right


# Scaling will be applied based on the smaller side	
def get_rectangle_size(height, width, scale):	
    if height < width:  # Scaling is applied based on height.
        return int(height * scale)
    # Scaling is applied based on the width.
    return int(width * scale)


def main():
    print("Excuse me?")


if __name__ == "__main__":
    main()
