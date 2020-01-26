#!/usr/bin/env python

"""drawing_utility.py: Module that takes one image and a position as an input, outputs the image with a shape/text drawn on it."""

# Imports
import cv2

# Information
__author__ = 	"Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = 	"Development"
__email__ =		"alaygut@gmail.com"

# Function that draws the rectangle.
# position: is a tuple (topLeft, bottomRight)
def draw_rectangle(image, position, color = (255, 0, 0), thickness = 1):
	return cv2.rectangle(image, position[0], position[1], color, thickness)

#Function that draws text.
def draw_text(image, text, bottomLeft, font = cv2.FONT_HERSHEY_SIMPLEX, scale = 1, color = (255, 0, 0), thickness = 1, lineType = cv2.LINE_AA):
	return cv2.putText(image, text, bottomLeft, font, scale, color, thickness, lineType)
