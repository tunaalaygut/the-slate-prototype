#!/usr/bin/env python
"""
pickle_loader.py: This module returns the object(s) stored in a pickle file.
"""

# Imports
import pickle

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


def get_pickle_object(path: str, mode="rb"):
    """Opens the file in the given path with the given mode
    (by default, in rb). Loads the object from the file using pickles, closes
    the file. Returns the object that is loaded by pickle.
    """
    file = open(path, mode)  # Open the file.
    pickle_object = pickle.load(file)  # Load the pickle.
    file.close()  # Close the file.
    return pickle_object


def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
