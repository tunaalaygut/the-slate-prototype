import eye
import calibration
import skin_detector
import cv2

while True:
	image = eye.see()
	(low_threshold, high_threshold) = calibration.get_thresholds()
	skinImage = skin_detector.get_skin_image(image, low_threshold, high_threshold)
	
	cv2.imshow("Trial", skinImage)

	key = cv2.waitKey(1)
			
	if key == 27:	#ESC key is pressed
		break
