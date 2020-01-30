#!/usr/bin/env python
"""
train_pegi.py: Trains the model with the specified architecture using the given
batch size, number of epochs and validation split.
"""

# Imports
import pickle
import os
import argparse
from classifier import pegi_architecture

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"

# Arguments to the program are defined below.
parser = argparse.ArgumentParser(description='')
parser.add_argument('-bs', '--batchsize', required=True, type=int,
                    help="Batch size to train with.")
parser.add_argument('-e', '--epochs', required=True, type=int,
                    help="Number of epoch to train for.")
parser.add_argument('-vs', '--validationsplit', required=True, type=int,
                    help="Validation split. Out of 100.")
args = vars(parser.parse_args())

batch_size = args["batchsize"]
epochs = args["epochs"]
validation_split = args["validationsplit"] / 100


def train_model():
    pickle_X_file = open("pickles/X.pickle", "rb")
    pickle_y_file = open("pickles/y.pickle", "rb")
    pickle_classes_file = open("pickles/classes.pickle", "rb")

    X = pickle.load(pickle_X_file)
    y = pickle.load(pickle_y_file)
    classes = pickle.load(pickle_classes_file)

    pickle_X_file.close()
    pickle_y_file.close()
    pickle_classes_file.close()

    X = X / 255.0  # Since X values are in grayscale.

    model = pegi_architecture.get_model(input_shape=X.shape[1:],
                                        output_size=len(classes),
                                        summarize=True)
    # Train the model.
    model.fit(X, y,
              batch_size=batch_size,
              epochs=epochs,
              validation_split=validation_split)

    # Save the model for future predictions.
    if not os.path.isdir("model_output"):
        os.mkdir("model_output")

    model.save("model_output/pegi.h5")


def main():
    train_model()
    print("Hello, World!")


if __name__ == "__main__":
    main()
