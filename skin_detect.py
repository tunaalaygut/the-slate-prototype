# Skin Detection using webcam. Color-based approach. Calibration based on user's skin tone.
import cv2
import numpy
import sdu
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pickle
from tensorflow import keras

#Global variables
LOW_THRESHOLD = []
HIGH_THRESHOLD = []

# Experimental offset values.
offsetLow = 20
offsetHigh = 30
OFFSET_UPDATE_AMOUNT = 5

SAMPLE_1 = []
SAMPLE_2 = []

ycrcb = cv2.COLOR_BGR2YCrCb
hsv = cv2.COLOR_BGR2HSV

COLOR_SPACE = ycrcb
calibrated = False


pickle_IMAGE_SIZE_file = open("../pegiv2/pickles/image_size.pickle", "rb")
pickle_CLASSES_file = open("../pegiv2/pickles/classes.pickle", "rb")

IMAGE_SIZE = pickle.load(pickle_IMAGE_SIZE_file)
CLASSES = pickle.load(pickle_CLASSES_file)

pickle_IMAGE_SIZE_file.close()
pickle_CLASSES_file.close()

model = keras.models.load_model("../pegiv2/model_output/pegi.h5")

def get_webcam_feed():
	global calibrated, SAMPLE_1, SAMPLE_2
	webcam = cv2.VideoCapture(0)	#Source is 0, can be passed as an argument to the program.
	print("\nWelcome to Slate's Skin Detector...\nWebcam feed started.")
	sdu.print_dashed_line()

	while True:
	
		captured, webcamImage = webcam.read()
		rectanglePosition = []	# Holds two tuples, x and y coordinates of the top-left and bottom-right corners of the sample area
		
		if not captured:
			print("Failed to capture a frame.")
			break
		
		if calibrated:
			thresholdImage = cv2.cvtColor(webcamImage, COLOR_SPACE)
			mask = cv2.inRange(thresholdImage, LOW_THRESHOLD, HIGH_THRESHOLD)
			
			# BELOW CODE IS NOT MINE!!!!
			# apply a series of erosions and dilations to the mask	
			# using an elliptical kernel
			kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
			mask = cv2.erode(mask, kernel, iterations = 2)
			mask = cv2.dilate(mask, kernel, iterations = 2)
			mask = cv2.GaussianBlur(mask, (3, 3), 0)
			
			skin = cv2.bitwise_and(webcamImage, webcamImage, mask=mask)
			#UNTIL HERE
			
			skin = cv2.flip(skin, 1)
			skin, predictionRectPos = sdu.draw_prediction_rectangle(skin)
			#finalImage = numpy.hstack([skin, webcamImage])
			#cv2.imshow("Webcam Feed", cv2.flip(finalImage, 1))
			cv2.imshow("Webcam Feed", skin)
			
			#pegi predicts grayscale
			imageToPredict = cv2.cvtColor(sdu.get_portion(skin, predictionRectPos), cv2.COLOR_BGR2GRAY)
			imageToPredict = cv2.resize(imageToPredict, IMAGE_SIZE)
			imageToPredict = imageToPredict.astype("float") / 255.0
			imageToPredict = imageToPredict.reshape((1, imageToPredict.shape[0], imageToPredict.shape[1], 1))
			
			prediction = model.predict(imageToPredict)

			index = prediction.argmax(axis=1)[0]
			label = CLASSES[index]
			percentage = numpy.amax(prediction) * 100
			if percentage > 80:
				print("It is a %%%.2f" % (numpy.amax(prediction) * 100) + " " + label + ".")
		else:
			webcamImage = cv2.flip(webcamImage, 1)
			webcamImage, sampleAreaOnePosition = sdu.draw_sample_rectangle(webcamImage, 1)
			webcamImage, sampleAreaTwoPosition = sdu.draw_sample_rectangle(webcamImage, 2)
			cv2.imshow("Webcam Feed", webcamImage)
		key = cv2.waitKey(1)
		
		if key == 27:	#ESC key is pressed
			break
		if key == 32:	#Space key is pressed
			print("Space")
		if key == 115:	# s key is pressed
			if not sdu.is_sample_set(SAMPLE_1):	#Sample 1 is not set
				#Set the SAMPLE 1
				SAMPLE_1 = sdu.set_sample(webcamImage, sampleAreaOnePosition)
				print("Sample image 1 is set.")
			else:
				if not sdu.is_sample_set(SAMPLE_2): #Sample 2 is not set
					#Set the SAMPLE 2, then calibrate.
					SAMPLE_2 = sdu.set_sample(webcamImage, sampleAreaTwoPosition)
					print("Sample image 2 is set.") 
					calibrate_user_skin_tone()
		update_offsets(key, OFFSET_UPDATE_AMOUNT)
	
	cv2.destroyAllWindows()
	
# Updates the THRESHOLDs based on user input
def update_offsets(key, amount):
	global offsetLow, offsetHigh, LOW_THRESHOLD, HIGH_THRESHOLD

	if key == 121 or key == 104 or key == 117 or key == 106:
		# First undo the current offset
		LOW_THRESHOLD = numpy.array([LOW_THRESHOLD[0] + offsetLow, LOW_THRESHOLD[1] + offsetLow, LOW_THRESHOLD[2] + offsetLow], dtype="uint8")
		HIGH_THRESHOLD = numpy.array([HIGH_THRESHOLD[0] - offsetHigh, HIGH_THRESHOLD[1] - offsetHigh, HIGH_THRESHOLD[2] - offsetHigh], dtype="uint8")

		if key == 121 and (offsetLow + amount) <= 255: #y, increase offsetLow
			offsetLow = offsetLow + amount
		if key == 104 and (offsetLow - amount) >= 0: #h, decrease offsetLow
			offsetLow = offsetLow - amount
		if key == 117 and (offsetHigh + amount) <= 255: #u, increase offsetHigh
			offsetHigh = offsetHigh + amount
		if key == 106 and (offsetHigh - amount) >= 0: #j, decrease offsetHigh
			offsetHigh = offsetHigh - amount	
		
		# Apply the new offset
		LOW_THRESHOLD = numpy.array([LOW_THRESHOLD[0] - offsetLow, LOW_THRESHOLD[1] - offsetLow, LOW_THRESHOLD[2] - offsetLow], dtype="uint8")
		HIGH_THRESHOLD = numpy.array([HIGH_THRESHOLD[0] + offsetHigh, HIGH_THRESHOLD[1] + offsetHigh, HIGH_THRESHOLD[2] + offsetHigh], dtype="uint8")
		
		print("Offsets and thresholds updated.")
		sdu.print_dashed_line()
		print("New low threshold:\t" + str(LOW_THRESHOLD))
		print("New high threshold:\t" + str(HIGH_THRESHOLD))
		print("New low offset:\t" + str(offsetLow))
		print("New high offset:\t" + str(offsetHigh))

def calibrate_user_skin_tone():
	global calibrated, LOW_THRESHOLD, HIGH_THRESHOLD
	print("Calibrating to user's skin tone.")
	sdu.print_dashed_line()
	
	# Make the calibration calculations here	
	sampleOneImage = cv2.cvtColor(SAMPLE_1, COLOR_SPACE)
	sampleTwoImage = cv2.cvtColor(SAMPLE_2, COLOR_SPACE)
	
	(LOW_THRESHOLD, HIGH_THRESHOLD) = sdu.calculate_thresholds_from_channels(cv2.mean(sampleOneImage), cv2.mean(sampleTwoImage), offsetLow, offsetHigh)
	
	# Ignore V in HSV color space
	if COLOR_SPACE == hsv:
		LOW_THRESHOLD[2] = 0
		HIGH_THRESHOLD[2] = 255
	# A heuristic value for Y component in YCrCb color space
	if COLOR_SPACE == ycrcb:
		LOW_THRESHOLD[0] = 0
		HIGH_THRESHOLD[0] = 235
	
	# Threshold Information is printed.
	print("Calibration is done.\n")
	sdu.print_dashed_line()
	print("Low Offset:\t" + str(offsetLow))
	print("High Offset:\t" + str(offsetHigh))
	print("Low Threshold:\t" + str(LOW_THRESHOLD))
	print("High Threshold:\t" + str(HIGH_THRESHOLD))
	calibrated = True

def main():
	get_webcam_feed()
	
if __name__ == "__main__":
	main()
