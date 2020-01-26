#!/usr/bin/env python

"""data_gatherer.py: Module that, given an image, output path and a filename, saves that image to the path with the given filename. Designed to use while creating datasets."""

# Imports
import cv2, time, argparse, os

# Information
__author__ = 	"Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = 	"Development"
__email__ =		"alaygut@gmail.com"

# Global variables.
limit = 9999

class DataGatherer:
	def __init__(self, outputFolderPath, filename, image_count = 0, limit = limit):
		self.outputFolderPath = outputFolderPath
		self.filename = filename
		self.image_count = image_count
		self.limit = limit
		
	# Saves the given image to the output path with the given filename.
	def save_image(self, image):
		if self.image_count < self.limit:
			image_name = (self.filename + "_{}.png").format(self.image_count)
			
			# Check if the driectory exists.
			if not os.path.isdir(self.outputFolderPath):
				# Directory does not exist, create it.
				os.makedirs(self.outputFolderPath)
				
			if cv2.imwrite(self.outputFolderPath + '/' + image_name, image):
				print("{} saved.".format(image_name))
			else:
				print("Image was not saved.")
			self.image_count += 1
		else:
			print (("Cannot save the image! Limit of {} is reached.").format(self.limit))
	
	# Returns the image count.
	def get_image_count(self):
		return self.image_count
