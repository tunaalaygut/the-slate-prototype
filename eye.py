#!/usr/bin/env python

"""eye.py: Module that handles the camera (webcam) stuff. Starts the webcam feed. Returns a frame from the webcam."""

# Imports
import cv2

# Information
__author__ = 	"Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = 	"Development"
__email__ =		"alaygut@gmail.com"

# Global variables
SOURCE = 0 # Default source is zero.
webcam = cv2.VideoCapture(SOURCE)

#Initialize the eye with a custom source.
def init_eye(source: int):
	global SOURCE, webcam
	SOURCE = source
	webcam = cv2.VideoCapture(SOURCE)

# see function returns the frame that camera sees at that moment. Can convert the image to given color space. By default returns a flipped image.
def see(flipped: bool = True, colorSpace = None): 
	captured, webcamImage = webcam.read()
	if captured:
		if colorSpace:
			webcamImage = cv2.cvtColor(webcamImage, colorSpace)
		if not flipped:
			return webcamImage
		return cv2.flip(webcamImage, 1)
	return None	
	
def main():
	print("Hello, World!")

if(__name__ == "__main__"):
	main()
