# Skin Detection using webcam.
import cv2
import numpy
import sdu

#Global variables
LOW_THRESHOLD = []
HIGH_THRESHOLD = []

SAMPLE_1 = []
SAMPLE_2 = []

ycrcb = cv2.COLOR_BGR2YCrCb
hsv = cv2.COLOR_BGR2HSV

COLOR_SPACE = hsv
calibrated = False

def get_webcam_feed():
	global calibrated, SAMPLE_1, SAMPLE_2
	webcam = cv2.VideoCapture(0)	#Source is 0, can be passed as an argument to the program.
	print("Webcam feed started.")
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
			
			finalImage = numpy.hstack([skin, webcamImage])
			cv2.imshow("Webcam Feed", cv2.flip(finalImage, 1))
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
	
	cv2.destroyAllWindows()
	
def calibrate_user_skin_tone():
	global calibrated, LOW_THRESHOLD, HIGH_THRESHOLD
	
	# Experimental offset values.
	offsetLow = 80
	offsetHigh = 30

	# Make the calibration calculations here	
	sampleOneImage = cv2.cvtColor(SAMPLE_1, COLOR_SPACE)
	sampleTwoImage = cv2.cvtColor(SAMPLE_2, COLOR_SPACE)
	
	# Find a proper way to find the mean, K-means clustering?
	sampleOneChannels = cv2.mean(sampleOneImage)
	sampleTwoChannels = cv2.mean(sampleTwoImage)
	
	# Necessary calculations for HSV color space.
	if(COLOR_SPACE == hsv):
		sampleOne_H = sampleOneChannels[0] 
		sampleOne_S = sampleOneChannels[1] 
		sampleOne_V = sampleOneChannels[2] 
		
		sampleTwo_H = sampleTwoChannels[0] 
		sampleTwo_S = sampleTwoChannels[1] 
		sampleTwo_V = sampleTwoChannels[2] 

		LOW_THRESHOLD = numpy.array([min(sampleOne_H, sampleTwo_H) - offsetLow, min(sampleOne_S, sampleTwo_S) - offsetLow, 0])
		HIGH_THRESHOLD = numpy.array([max(sampleOne_H, sampleTwo_H) + offsetHigh, max(sampleOne_S, sampleTwo_S) + offsetHigh, 255])
	
	# Information is printed.
	print("Sample one channels: " + str(sampleOneChannels))
	print("Sample two channels: " + str(sampleTwoChannels))
	print("Low Threshold: " + str(LOW_THRESHOLD))
	print("High Threshold: " + str(HIGH_THRESHOLD))
	calibrated = True

def main():
	get_webcam_feed()
	
if __name__ == "__main__":
	main()
