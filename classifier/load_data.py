#!/usr/bin/env python
"""
load_data.py: Module that loads the data from a given data set path. This
module loads data that has the following structure:
    dataSetPath
    ---> classLabelDirectory
        ---> file.ext
It loads the data with the corresponding class label, then binarizes the labels
for later categorical classification.
"""

# Imports
import numpy
import os
import cv2
import random
import pickle
from tensorflow.keras import utils as np_utils

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"

data_dir = "./dataset"
image_size = (80, 80)
load_threshold = 1000  # Load no more than this amount of file per class.

# Global variables
classes = []
training_data = []

# Since, y is a function of X.
X = []  # For the data
y = []  # For the label


# Loads the CLASSES list based on the folders inside data set folder
def load_classes():
    for CLASS in os.listdir(data_dir):
        classes.append(CLASS)


# Loads the dataset to training_data array.
def create_training_data():
    load_classes()
    for CLASS in classes:
        path = os.path.join(data_dir, CLASS)
        class_index = classes.index(CLASS)
        count = 0
        for image in os.listdir(path):
            # Do not load past the threshold
            if count >= load_threshold:
                break
            # Load the actual images and append them to training_data.
            try:
                image_array = cv2.resize(cv2.imread(os.path.join(path, image),
                                                    cv2.IMREAD_GRAYSCALE),
                                         image_size)
                training_data.append([image_array, class_index])
                count += 1
            except Exception as e:
                pass

    # Shuffle the training_data array.
    random.shuffle(training_data)


def main():
    global X, y
    create_training_data()

    for data, label in training_data:
        X.append(data)
        # Convert the labels to binary to use them
        # with categorical_crossentropy
        y.append(np_utils.to_categorical(label, num_classes=len(classes)))

    X = numpy.array(X).reshape(-1, (image_size[0], image_size[1]), 1)
    y = numpy.array(y)

    store_data()

    print("{} data images loaded successfully.".format(len(X)))
    print("With {} labels: {}".format(len(classes), classes))


def store_data():
    # Save the data so you don't have to load it every time.
    if not (os.path.isdir("pickles")):
        os.mkdir("pickles")

    pickle_output = open("pickles/X.pickle", "wb")
    pickle.dump(X, pickle_output)
    pickle_output.close()

    pickle_output = open("pickles/classes.pickle", "wb")
    pickle.dump(classes, pickle_output)
    pickle_output.close()

    pickle_output = open("pickles/y.pickle", "wb")
    pickle.dump(y, pickle_output)
    pickle_output.close()

    pickle_output = open("pickles/image_size.pickle", "wb")
    pickle.dump(image_size, pickle_output)
    pickle_output.close()

    print("Stored the pickles.")


if __name__ == "__main__":
    main()
