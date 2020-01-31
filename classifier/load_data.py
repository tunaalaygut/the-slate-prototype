#!/usr/bin/env python
"""
load_data.py: Module that loads the data from a given data set path. This
module loads data that has the following structure:
    dataSetPath
    ---> classLabelDirectory
        ---> file.ext
It loads the data with the corresponding class label, then binarizes the labels
for later categorical classification.
Loads the images in GRAYSCALE.
"""

# Imports
import numpy
import os
import cv2
import random
import argparse
from tensorflow.keras import utils
from classifier.pickle_utility import put_pickle_object

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"

# Arguments to the program are defined below.
parser = argparse.ArgumentParser(description='')
parser.add_argument('-d', '--dataset', required=True,
                    help="Path to the data set directory.")
parser.add_argument('-ih', '--height', required=True, type=int,
                    help="Desired height of dataset images.")
parser.add_argument('-iw', '--width', required=True, type=int,
                    help="Desired width of dataset images.")
# Load no more than this amount of file per class.
parser.add_argument('-t', '--threshold', type=int, default=1000,
                    help="Path to the data set directory.")
args = vars(parser.parse_args())

data_dir = args["dataset"]
image_size = (args["height"], args["width"])
load_threshold = args["threshold"]

# Global variables
classes = []
training_data = []

# Since, y is a function of X.
X = []  # For the data
y = []  # For the label


# Loads the CLASSES list based on the folders inside data set folder
def load_classes():
    global classes
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
        y.append(utils.to_categorical(label, num_classes=len(classes)))

    X = numpy.array(X).reshape(-1, *image_size, 1)
    y = numpy.array(y)

    store_data()

    print("{} data images loaded successfully.".format(len(X)))
    print("With {} labels: {}".format(len(classes), classes))


def store_data():
    # Save the data so you don't have to load it every time.
    if not (os.path.isdir("pickles")):
        os.mkdir("pickles")

    put_pickle_object(X, "pickles/X.pickle")
    put_pickle_object(classes, "pickles/classes.pickle")
    put_pickle_object(y, "pickles/y.pickle")
    put_pickle_object(image_size, "pickles/image_size.pickle")

    print("Stored the pickles.")


if __name__ == "__main__":
    main()
