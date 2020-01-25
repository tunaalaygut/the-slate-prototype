#!/usr/bin/env python

"""model_service.py: Module that, takes a .h5 model (pegi, in our case) and a image and outputs the model's prediction on that image."""

# Imports
import cv2
import numpy as np

# Information
__author__ = 	"Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = 	"Development"
__email__ =		"alaygut@gmail.com"

# Function that returns a model's prediction (as a string (label) and it's probability (percentage))
# model: model to make predictions with
# image: image to be fed to the model to get a prediction
# imageSize: what is the image size that the model expects?
# labels: labels of the output classes of the model.
# colorSpace: in which color space does the model work? 
def get_prediction(model, image, imageSize, labels, colorSpace):
	# Necessary transformations to the image
	image = cv2.cvtColor(image, colorSpace)
	image = cv2.resize(image, imageSize)
	image = image.astype("float") / 255
	
	# What does this line DO?
	image = image.reshape(1, image.shape[0], image.shape[1], 1)
	
	prediction = model.predict(image)
	
	index = prediction.argmax(axis=1)[0]
	label = labels[index]
	percentage = np.amax(prediction) * 100
	
	return (label, percentage)

def get_formatted_prediction(model, image, imageSize, labels, colorSpace):
	(label, percentage) = get_prediction(model, image, imageSize, labels, colorSpace)
	
	return ("It is a %%%.2f" % (percentage) + " " + label + ".")
	
def main():
	print("Excuse me?")

if (__name__ == "__main__"):
	main()
