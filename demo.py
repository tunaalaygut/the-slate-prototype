#!/usr/bin/env python

from detector import eye
from detector import calibration
from detector import skin_detector
from detector import drawing_utility
from detector import sampler
from detector import model_service
from tensorflow import keras
from detector import data_gatherer

import cv2
import pickle
from time import sleep
from sys import stdout

samplePositions = []

sampleAreaOnePosition = ((25, 25), (125, 125))
sampleAreaTwoPosition = ((400, 25), (500, 125))

predictionAreaPosition = ((100, 100), (400, 400))

samplePositions.append(sampleAreaOnePosition)
samplePositions.append(sampleAreaTwoPosition)

samplesToTake = len(samplePositions)
samplesTaken = 0

sampleImages = []

CALIBRATED = False

LOW_THRESHOLD = []
HIGH_THRESHOLD = []

windowTitle = "P.E.G.I. & Skin Detection Demo"

pickle_IMAGE_SIZE_file = open("./classifier/pickles/image_size.pickle", "rb")
pickle_CLASSES_file = open("./classifier/pickles/classes.pickle", "rb")

IMAGE_SIZE = pickle.load(pickle_IMAGE_SIZE_file)
CLASSES = pickle.load(pickle_CLASSES_file)

pickle_IMAGE_SIZE_file.close()
pickle_CLASSES_file.close()

model = keras.models.load_model("./classifier/model_output/pegi.h5")

data_gatherer = data_gatherer.DataGatherer("./gestures/fbomb", "fbomb", limit = 5)

print("Welcome to P.E.G.I. & Skin Detection Demo\n-----------------------------------------\n")

while True:
	image = eye.see()
	
#	(low_threshold, high_threshold) = calibration.get_thresholds()
#	skinImage = skin_detector.get_skin_image(image, low_threshold, high_threshold)
	imageR = image.copy()
	imageR = drawing_utility.draw_rectangle(imageR, sampleAreaOnePosition, thickness = 2)
	imageR = drawing_utility.draw_rectangle(imageR, sampleAreaTwoPosition, thickness = 2, color = (0, 0, 255))
	
	if CALIBRATED:
		#WHY???? YCrCb study might explain
		LOW_THRESHOLD[0] = 0
		HIGH_THRESHOLD[0] = 235
		finalImage = skin_detector.get_skin_image(image, LOW_THRESHOLD, HIGH_THRESHOLD)
		finalImage = drawing_utility.draw_rectangle(finalImage, predictionAreaPosition, thickness = 2, color = (255, 255, 0))
		
		predictionImage = sampler.get_sample_image(finalImage, predictionAreaPosition)
		predictionText, percentage = model_service.get_prediction(model, predictionImage, IMAGE_SIZE, CLASSES, cv2.COLOR_BGR2GRAY)
		
		if percentage > 90:		
			finalImage = drawing_utility.draw_text(finalImage, ("It is {} {}").format(predictionText, percentage), (predictionAreaPosition[0][0], predictionAreaPosition[1][1] + 20), scale = 0.8, color = (0, 0, 255), thickness = 2)
		
		cv2.imshow(windowTitle, finalImage)
	else:
		cv2.imshow(windowTitle, imageR)
		
	key = cv2.waitKey(1)
			
	if key == 27:	#ESC key is pressed
		break
	if key == 32: # Space key is pressed
		data_gatherer.save_image(image)
	if key == 115 and not CALIBRATED:	# s key is pressed and calibration is not done yet.
		if samplesTaken < samplesToTake:
			sampleImage = sampler.get_sample_image(image, samplePositions[samplesTaken])
			sampleImages.append(sampleImage)
			samplesTaken += 1
			print(("Sample {} is taken.").format(samplesTaken))
			if(samplesTaken == samplesToTake):
				print("\nPress s to start skin detection...\n")
		else:
			LOW_THRESHOLD, HIGH_THRESHOLD = calibration.get_thresholds(sampleImages)
			print("\nSkin detection started now.")
			CALIBRATED = True
cv2.destroyAllWindows()
