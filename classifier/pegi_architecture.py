#!/usr/bin/env python
"""
pegi_architecture.py: Module that defines the architecture of the pegi neural
network.
"""

# Imports
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D,\
    Activation, Flatten, Dense

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


def get_model(input_shape, output_size, summarize=False):
    """Returns the model with the specified input and output size."""
    model = Sequential()

    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2, 2))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2, 2))

    model.add(Conv2D(128, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2, 2))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))

    model.add(Dense(output_size))
    model.add(Activation('softmax'))

    # Configure the model.
    model.compile(loss="categorical_crossentropy",
                  optimizer="adam",
                  metrics=["accuracy"])

    if summarize:
        model.summary()	 # Prints the summary of the model before returning.

    return model


def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()