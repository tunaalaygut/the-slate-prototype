#!/usr/bin/env python

"""skin_detector.py: Module that, given an image and two thresholds (low and high), produces an image that is showing all the skin pixels and masking all the non-skin pixels."""

# Imports
import cv2
import numpy as np

# Information
__author__ = 	"Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = 	"Development"
__email__ =		"alaygut@gmail.com"

# Returns the skin image.
def get_skin_image(image, lowThreshold, highThreshold, colorSpace = cv2.COLOR_BGR2YCrCb):
	skinImage = apply_thresholding(image, lowThreshold, highThreshold, colorSpace)
	return skinImage

# Function that does the actual thresholding. Leaves out the areas of the image that are not inside the specified thresholds.
def apply_thresholding(image, lowThreshold, highThreshold, colorSpace):
	thresholdImage = cv2.cvtColor(image, colorSpace)
	
	mask = cv2.inRange(thresholdImage, lowThreshold, highThreshold)
	mask = morphologicalOperations(mask)
	
	return cv2.bitwise_and(image, image, mask=mask)
	
# Morphological operations, they need to inputs; one the image to apply the operation to and second the kernel or a structuring element which decides the nature of the operation.
def morphologicalOperations(image):
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
	
	image = cv2.erode(image, kernel, iterations = 2)
	image = cv2.dilate(image, kernel, iterations = 2)
	image = cv2.GaussianBlur(image, (3, 3), 0)
	
	return image
	
