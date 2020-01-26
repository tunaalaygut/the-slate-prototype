#!/usr/bin/env python

"""position_provider.py: Module that, provides positions to be used when drawing rectangles in the form of a tuple (topLeft, bottomRight).
Positions are calculated based on the frame size. Difference between points is based on the scale input."""

# Imports
import cv2
import numpy as np

# Information
__author__ = 	"Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = 	"Development"
__email__ =		"alaygut@gmail.com"

#  Returns the suitable position of a rectangle that can be drawn on the top left
# of the given image.
# image: image that the rectangle will be drawn on top of.
# scale: scale of the rectangle wrt the smaller side of the image.
# padding: padding to be left on the top and left of the image.
def get_top_left(image, scale = 0.25, padding = 25):
	(height, width, _) = image.shape
	
	rectangle_size = get_rectangle_size(height, width, scale)
		
	topLeft = (padding, padding)
	bottomRight = (padding + rectangle_size, padding + rectangle_size)
	
	return (topLeft, bottomRight)
	
#  Returns the suitable position of a rectangle that can be drawn on the top right
# of the given image.
# parameters are same as get_top_left function
def get_top_right(image, scale = 0.25, padding = 25):
	(height, width, _) = image.shape
	
	rectangle_size = get_rectangle_size(height, width, scale)
		
	topLeft = (width - (padding + rectangle_size), padding)
	bottomRight = (width - padding, padding + rectangle_size)
	
	return (topLeft, bottomRight)

#  Returns the positions of the rectangle that can be drawn on the
# center of an image.
def get_center(image, scale = 0.25):
	(height, width, _) = image.shape
	rectangle_size = get_rectangle_size(height, width, scale)
	
	centerX = int(width/2) 
	centerY = int(height/2)
	
	topLeft = (centerX - int(rectangle_size/2), centerY - int(rectangle_size/2))
	bottomRight = (centerX + int(rectangle_size/2), centerY + int(rectangle_size/2))
	
	return (topLeft, bottomRight)

# Scaling will be applied based on the smaller side	
def get_rectangle_size(height, width, scale):	
	if(height < width): # scaling is applied based on height
		return int(height * scale)
	# scaling is applied based on the width 
	return int(width * scale)	
		
def main():
	print("Excuse me?")

if (__name__ == "__main__"):
	main()
