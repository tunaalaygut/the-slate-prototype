#!/usr/bin/env python

"""
eye.py: Module that handles the camera (webcam) stuff. Starts the webcam feed.
Returns a frame from the webcam.
"""

# Imports
import cv2

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


class Eye:
    def __init__(self, source: int = 0):
        self.webcam = cv2.VideoCapture(source)

    def see(self, flipped: bool = True, color_space=None):
        """
        Provides a frame from the eye (camera).

        Args:
            flipped: Flip the returned image or not.
            color_space: Which color space to see in.

        Returns:
            The image captured by the webcam.
        """
        captured, webcam_image = self.webcam.read()
        if captured:
            if color_space:
                webcam_image = cv2.cvtColor(webcam_image, color_space)
            if not flipped:
                return webcam_image
            return cv2.flip(webcam_image, 1)
        return None

    def set_source(self, source):
        """
        This function can be called if there is a need to change the camera
        source.

        Args:
            source: New source of the webcam.
        """
        self.webcam = cv2.VideoCapture(source)

    def release(self):
        """ When done, release the capture. """
        self.webcam.release()


def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
