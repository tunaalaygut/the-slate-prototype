#!/usr/bin/env python

"""calibration.py: Module that, given a list of sample images, calculates the low and high thresholds that pixels need to fall in between in order to be similar to the given sample images."""

# Imports
import cv2
import numpy as np

# Information
__author__ = 	"Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = 	"Development"
__email__ =		"alaygut@gmail.com"

# Global variables
# Experimental default values.
LOW_THRESHOLD 	= np.array([0, 133, 77], dtype = "uint8")
HIGH_THRESHOLD	= np.array([235, 173, 127], dtype = "uint8")
OFFSET_LOW 	= 20
OFFSET_HIGH = 30

# First calculates then returns the LOW_THRESHOLD and HIGH_THRESHOLD as a tuple.
# offsetLow: Give the low offset as an argument. If not specificed default value will be used.
# offsetHigh: Give the high offset as an argument. If not specificed default value will be used.
def get_thresholds(sampleImages = None, offsetLow = OFFSET_LOW, offsetHigh = OFFSET_HIGH):
	if sampleImages:
		calculate_thresholds(sampleImages, offsetLow, offsetHigh)
	return (LOW_THRESHOLD, HIGH_THRESHOLD)

# Calculates the thresholds based on the given sample images.
def calculate_thresholds(sampleImages, offsetLow, offsetHigh):
	global LOW_THRESHOLD, HIGH_THRESHOLD
	
	LOW_THRESHOLD = calculate_threshold(sampleImages, True, offsetLow)
	HIGH_THRESHOLD = calculate_threshold(sampleImages, False, offsetHigh)

# Calculates a single threshold.
# isLow: set this True if low threshold is being calculated. False if high is being calculated.
# offset: offset value. When calculating the low threshold offset will be subtracted, when calculating high threshold it will be added.
def calculate_threshold(sampleImages, isLow: bool, offset):
	firstChannels = []
	secondChannels = []
	thirdChannels = []
	
	for image in sampleImages:
		meanChannels = cv2.mean(image) # Mean value of each channel in the image.
		firstChannels.append(meanChannels[0])
		secondChannels.append(meanChannels[1])
		thirdChannels.append(meanChannels[2])
	
	if(isLow):	# Low threshold is being calculated.
		return np.array([min(firstChannels) - offset, min(secondChannels) - offset, min(thirdChannels) - offset], dtype = "uint8")
	
	# High threshold is being calculated.
	return np.array([max(firstChannels) + offset, max(secondChannels) + offset, max(thirdChannels) + offset], dtype = "uint8")
	
def main():
	print("Excuse me?")
	
if __name__ == "__main__":
	main()
	
