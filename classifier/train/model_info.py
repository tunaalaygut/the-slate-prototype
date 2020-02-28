#!/usr/bin/env python
"""
model_info.py: This module takes a model and it's name. Creates a directory for
the model, save the model inside that directory as a .h5 file. Creates a .info
file about the model.
.info file includes: Model's name, date of training and summary.
"""

# Imports
import time

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


def save_model(model, path: str, model_name: str):
    """
    Saves the model with relevant information to a directory.

    Args:
        model: Model to save.
        path: Where to save the model.
        model_name: Name of the model.
    """

    model.save("{}/{}.h5".format(path, model_name))
    create_info_file(model, model_name, path)


def create_info_file(model, model_name, path):
    info_file = open("{}/{}.info".format(path, model_name), "a+")
    training_time = str(time.strftime("%d-%m-%Y  %H:%M:%S", time.localtime()))
    info_file.write("*This model ({}) was trained on {}.\n\n\n"
                    .format(model_name, training_time))
    # What does the following line do?
    model.summary(print_fn=lambda x: info_file.write(x + '\n'))
    info_file.close()


def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
