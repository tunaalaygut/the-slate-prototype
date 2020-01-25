#!/usr/bin/env python

"""sampler.py: Module that takes one image and a list of positions as input and outputs a list of sample images (portions of the input image with the given positions)."""

# Information
__author__ = 	"Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = 	"Development"
__email__ =		"alaygut@gmail.com"

# Function that will be called.
# image: The image that will be used to take samples from.
# positions: List of positions. Each position is a tuple (topLeft, bottomRight).
def get_sample_images(image, positions):
	samples = []
	
	for position in positions:
		samples.append(get_sample_image(image, position))
		
	return samples

# returns a single portion of an image.
def get_sample_image(image, position):
	topLeftX = get_top_left(position)[0];
	topLeftY = get_top_left(position)[1];
	
	bottomRightX = get_bottom_right(position)[0];
	bottomRightY = get_bottom_right(position)[1];

	return image[topLeftY + 2 : bottomRightY - 2, topLeftX + 2 : bottomRightX - 2]

# Takes a position and returns the top left corner.
def get_top_left(position):
	return (position[0][0], position[0][1])
	
# Takes a position and returns the bottom right corner.
def get_bottom_right(position):
	return (position[1][0], position[1][1])
