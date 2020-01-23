#Skin Detection Utilities (sdu) by Tuna ALAYGUT 20.01.2020
import cv2

#Draws a sampling rectangle on a frame and returns the frame and rectangle position.
def draw_sample_rectangle(image, number):

	(height, width, depth) = image.shape
	rectSize = 100

	if number == 1:
		rectStartPoint = (25, 25)
		rectEndPoint = (rectStartPoint[0] + rectSize, rectStartPoint[0] + rectSize)
		rectColor = (139, 0, 139)
	else:	# Assume that there can only be two sample areas, either 1 or 2
		rectStartPoint = (width-(25 + rectSize), 25)
		rectEndPoint = (width - 25, rectSize + 25)
		rectColor = (0, 139, 0) 
		
	position = (rectStartPoint, rectEndPoint)
	rectThickness = 2
	
	rectText = "Sample Area " + str(number)
	rectTextBottomLeft = (rectStartPoint[0], rectEndPoint[1] + 15)
	rectTextFont = cv2.FONT_HERSHEY_SIMPLEX
	rectTextScale = 0.35
	rectTextColor = rectColor
	rectTextThickness = 1
	rectTextLineType = cv2.LINE_AA

	image = cv2.putText(image, rectText, rectTextBottomLeft, rectTextFont, rectTextScale, rectTextColor, rectTextThickness, rectTextLineType)
	return (cv2.rectangle(image, rectStartPoint, rectEndPoint, rectColor, rectThickness), position)
	
# Takes a position and returns the top left corner.
def get_top_left(position):
	return (position[0][0], position[0][1])
# Takes a position and returns the bottom right corner.
def get_bottom_right(position):
	return (position[1][0], position[1][1])

# Returns True if a sample is set
def is_sample_set(sample):
	return len(sample) != 0
	
# Given two numbers, makes the offset calculation and fits the result between [0-255].
# isAddition: whether the offset will be added or not.
def fit_to_0_255(a, b, offset, isAddition):
	if not isAddition:
		offset = -1 * offset
		func = min
	else:
		func = max
	
	return get_uint8( func(a, b) + offset)

# Takes a number fits it to 8 bit.
def get_uint8(number):
	if(number < 0):
		return 0
	if(number > 255):
		return 255
	return number	

# Returns a portion, with the given position(top left and bottom right), of an image.
def get_portion(image, position):

	topLeftX = get_top_left(position)[0];
	topLeftY = get_top_left(position)[1];
	
	bottomRightX = get_bottom_right(position)[0];
	bottomRightY = get_bottom_right(position)[1];

	return image[topLeftY + 2 : bottomRightY - 2, topLeftX + 2 : bottomRightX - 2]

# Prints a dashed line and a new line.
def print_dashed_line():
	print("-----------------------\n")

# Extracts the sample image from its position
def set_sample(image, sampleAreaPosition):
	return get_portion(image, sampleAreaPosition)
	
	
	
