#!/usr/bin/env python
"""
pickle_utility.py: This module returns the object(s) stored in a pickle file.
"""

# Imports
import pickle

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


def get_pickle_object(path: str, mode="rb"):
    """
    Opens the file in the given path with the given mode
    (by default, in rb). Loads the object from the file using pickles, closes
    the file. Returns the object that is loaded by pickle.

    Args:
        path: Path to load the file from.
        mode: Mode to open the file with.
    """
    file = open(path, mode)  # Open the file.
    pickle_object = pickle.load(file)  # Load the pickle.
    file.close()  # Close the file.
    return pickle_object


def put_pickle_object(obj, path: str, mode="wb"):
    """
    Stores an object using pickles.

    Args:
        obj: Object to store.
        path: Path to store the pickle file.
        mode: Mode to open the file with.
    """
    file = open(path, mode)
    pickle.dump(obj, file)
    file.close()


def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
