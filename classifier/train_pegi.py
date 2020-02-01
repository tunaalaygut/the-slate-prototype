#!/usr/bin/env python
"""
train_pegi.py: Trains the model with the specified architecture using the given
batch size, number of epochs and validation split.
"""

# Imports
import os
import argparse
import time
from classifier import pegi_architecture
from classifier.pickle_utility import get_pickle_object
from classifier import model_info
from tensorflow.keras.callbacks import TensorBoard

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
parser.add_argument('-mn', '--modelname', required=True,
                    help="Name of the model. Specify architecture briefly.")
args = vars(parser.parse_args())

# Give model a unique name. Append time to the end.
MODEL_NAME = "PEGI-{}-{}".format(args["modelname"], int(time.time()))

batch_size = args["batchsize"]
epochs = args["epochs"]
validation_split = args["validationsplit"] / 100

output_dir = "model_output"

x = []
y = []
classes = []

tensorboard = TensorBoard(log_dir="{}/logs/{}".format(output_dir, MODEL_NAME))


def train_model():
    global x

    load_data()

    x = x / 255.0  # Since X values are in grayscale.

    model = pegi_architecture.get_model(input_shape=x.shape[1:],
                                        output_size=len(classes),
                                        summarize=False)

    directory_name = "{}/{}".format(output_dir, MODEL_NAME)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)

    # Train the model.
    model.fit(x, y,
              batch_size=batch_size,
              epochs=epochs,
              validation_split=validation_split,
              callbacks=[tensorboard])

    model_info.save_model(model, directory_name, MODEL_NAME)


def load_data():
    global x, y, classes

    x = get_pickle_object("pickles/X.pickle")
    y = get_pickle_object("pickles/y.pickle")
    classes = get_pickle_object("pickles/classes.pickle")


def main():
    train_model()


if __name__ == "__main__":
    main()
