#!/usr/bin/env python

"""
data_gatherer.py: Module that, given an image, output path and a filename,
saves that image to the path with the given filename.
Designed to be used while creating datasets.
"""

# Imports
import cv2
import os

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"

# Global variables.
LIMIT = 9999


class DataGatherer:
    def __init__(self, output_path, filename, image_count=0, limit=LIMIT, extension="png"):
        """
        Initializes the instance with the necessary information to
        save the image.

        Args:
            output_path: Path to save the image to.
            filename: Name of the image.
            image_count: Start counting from...
            limit: Limit of the number of images to save.
        """
        self.outputFolderPath = output_path
        self.filename = filename
        self.image_count = image_count
        self.limit = limit
        self.extension = extension

    def save_image(self, image):
        """
        Saves the given image to the output path with the given filename.

        Args:
            image: Image to save.
        """
        if self.image_count < self.limit:
            image_name = f"{self.filename}_{self.image_count}.{self.extension}"
            # Check if the directory exists.
            if not os.path.isdir(self.outputFolderPath):
                # Directory does not exist, create it.
                os.makedirs(self.outputFolderPath)

            if cv2.imwrite(self.outputFolderPath + '/' + image_name, image):
                print("{} saved.".format(image_name))
            else:
                print("Image was not saved.")
            self.image_count += 1
        else:
            print("Cannot save the image! Limit of {} is reached."
                  .format(self.limit))

    # Returns the image count.
    def get_image_count(self):
        return self.image_count


def main():
    print("Excuse me?")


if __name__ == "__main__":
    main()
