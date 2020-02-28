#!/usr/bin/env python

"""
drawing_utility.py: Module that takes one image and a position as an input,
outputs the image with a shape/text drawn on it.
"""

# Imports
import cv2

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"

# Global variables
default_color = (255, 0, 0)  # I like red.


def draw_rectangle(image, position, color=default_color, thickness=1):
    """
    Function that draws the rectangle.

    Args:
        image: Image to draw the rectangle on top of.
        position: Position on the image the draw the rectangle.
        color: Color of the rectangle.
        thickness: Thickness of the rectangle.

    Returns:
        The same image with a rectangle drawn on top of it.
    """
    return cv2.rectangle(image, position[0], position[1], color, thickness)


def draw_text(image, text: str, bottom_left, font=cv2.FONT_HERSHEY_SIMPLEX,
              scale=1, color=default_color, thickness=1,
              line_type=cv2.LINE_AA):
    """
    Function that draws text on top of an image.

    Args:
        image: Image to draw the text on top of.
        text: String that will be drawn on top of the image.
        bottom_left: Bottom left position of the text.
        font: Font to use.
        scale: Scale it wrt default size of the text.
        color: Color of the text.
        thickness: Thickness of the text.
        line_type: Line type of the text.

    Returns:
        The same image with the text drawn on top of it.
    """
    return cv2.putText(image, text, bottom_left, font, scale, color, thickness,
                       line_type)


def main():
    print("Hello, world!")


if __name__ == '__main__':
    main()
