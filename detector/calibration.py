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
OFFSET_HIGH = 20

# First calculates then returns the LOW_THRESHOLD and HIGH_THRESHOLD as a tuple.
# offsetLow: Give the low offset as an argument. If not specificed default value will be used.
# offsetHigh: Give the high offset as an argument. If not specificed default value will be used.
# colorSpace : in which color space do you want the threshold calculations be made? By default it is YCrCb.
def get_thresholds(sampleImages = None, offsetLow = OFFSET_LOW, offsetHigh = OFFSET_HIGH, colorSpace = cv2.COLOR_BGR2YCrCb):
	if sampleImages:
		calculate_thresholds(sampleImages, offsetLow, offsetHigh, colorSpace)
		# Print some information regarding the calculation results
		print("With offsets\n------------------")
		print("offsetLow:\t" + str(offsetLow))
		print("offsetHigh:\t" + str(offsetHigh))
		print("\nTresholds are calculated as\n-----------------------------")
		print("LOW_THRESHOLD:\t"+ str(LOW_THRESHOLD))
		print("HIGH_THRESHOLD:\t"+ str(HIGH_THRESHOLD))
	else:
		print("Default threshold values are returned.")
	return (LOW_THRESHOLD, HIGH_THRESHOLD)

# Calculates the thresholds based on the given sample images.
def calculate_thresholds(sampleImages, offsetLow, offsetHigh, colorSpace):
	global LOW_THRESHOLD, HIGH_THRESHOLD
	
	LOW_THRESHOLD = calculate_threshold(sampleImages, True, offsetLow, colorSpace)
	HIGH_THRESHOLD = calculate_threshold(sampleImages, False, offsetHigh, colorSpace)

# Calculates a single threshold.
# isLow: set this True if low threshold is being calculated. False if high is being calculated.
# offset: offset value. When calculating the low threshold offset will be subtracted, when calculating high threshold it will be added.
def calculate_threshold(sampleImages, isLow: bool, offset, colorSpace):
	firstChannels = []
	secondChannels = []
	thirdChannels = []
	
	for image in sampleImages:
		image = cv2.cvtColor(image, colorSpace)
		meanChannels = cv2.mean(image) # Mean value of each channel in the image.
		firstChannels.append(meanChannels[0])
		secondChannels.append(meanChannels[1])
		thirdChannels.append(meanChannels[2])
	
	if(isLow):	# Low threshold is being calculated.
		return np.array([fit(firstChannels, offset, False), fit(secondChannels, offset, False), fit(thirdChannels, offset, False)], dtype = "uint8")
	
	# High threshold is being calculated.
	return np.array([fit(firstChannels, offset, True), fit(secondChannels, offset, True), fit(thirdChannels, offset, True)], dtype = "uint8")

# Fits the result of threshold calculations between 0 and 255.
def fit(a, offset, isAddition):
	print(a, isAddition)
	if not isAddition:
		offset = -1 * offset
		func = min
	else:
		func = max
	
	return get_uint8( func(a) + offset)	
	
# Takes a number fits it to 8 bit.
def get_uint8(number):
	if(number < 0):
		return 0
	if(number > 255):
		return 255
	return number	
	
def main():
	print("Excuse me?")
	
if __name__ == "__main__":
	main()
	
