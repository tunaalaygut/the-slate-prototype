#!/usr/bin/env python

"""
model_service.py: Module that, takes a .h5 model (pegi, in our case) and an
image and outputs the model's prediction on that image. It also has the PEGI
class which uses this module's prediction function to make predictions.
"""

# Imports
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


class PEGI:  # Primary, Excellent Gesture Identifier
    """
    PEGI class. Contains the model which is a .h5 model,
    loaded from the model_path.
    """
    def __init__(self, model_path, image_size, labels, color_space):
        self.model = load_model(model_path)
        self.image_size = image_size
        self.labels = labels
        self.color_space = color_space

    def predict(self, image):
        """
        Uses classes model to make prediction on an image.
        Args:
            image: Image to perdict.

        Returns:
            label: What the model predicted.
            percentage: Model's confidence on the prediction.
        """
        return get_prediction(self.model,
                              image,
                              self.image_size,
                              self.labels,
                              self.color_space)


def get_prediction(model, image, image_size, labels, color_space):
    """
    Function that returns a model's prediction (as a string (label) and it's
    probability (percentage)).
    Args:
        model: Model to make the prediction with.
        image: Image to feed to the model to make the prediction.
        image_size: Input image size of the model.
        labels: Class labels of the model.
        color_space: Color space that the model makes predictions in.

    Returns:
        Class label of the prediction and the probability of the prediction.
    """
    # Necessary transformations to the image
    image = cv2.cvtColor(image, color_space)
    image = cv2.resize(image, image_size)
    image = image.astype("float") / 255

    # What does this line DO?
    image = image.reshape(1, image.shape[0], image.shape[1], 1)

    prediction = model.predict(image)

    index = prediction.argmax(axis=1)[0]
    label = labels[index]
    percentage = np.amax(prediction) * 100

    return label, percentage


def get_formatted_prediction(model, image, image_size, labels, color_space):
    """
    Function that returns a model's prediction as a formatted string. Can be
    used to directly display the prediction.
    Args:
        model: Model to make the prediction with.
        image: Image to feed to the model to make the prediction.
        image_size: Input image size of the model.
        labels: Class labels of the model.
        color_space: Color space that the model makes predictions in.

    Returns:
        The prediction of the model as a formatted string.
    """
    (label, percentage) = get_prediction(model, image, image_size, labels,
                                         color_space)

    return "It is a %%%.2f" % percentage + " " + label + "."


def main():
    print("Excuse me?")


if __name__ == "__main__":
    main()
