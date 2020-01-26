import numpy
import os
import matplotlib.pyplot as plt
import cv2
import random
import pickle
from tensorflow.keras import utils as np_utils

DATA_DIRECTORY = "./dataset"
IMAGE_SIZE = (80, 80)
DATA_SET_LOAD_EQUALIZER = 1000

#Global lists
CLASSES = []
training_data = []

#loads the CLASSES list based on the folders inside dataset folder
def load_classes():
	for CLASS in os.listdir(DATA_DIRECTORY):
		CLASSES.append(CLASS)

#Loads the dataset to training_data array.
def create_training_data():
	load_classes()
	for CLASS in CLASSES:
		path = os.path.join(DATA_DIRECTORY, CLASS)
		class_index = CLASSES.index(CLASS)
		count = 0
		for image in os.listdir(path):
			#Do not load past the threshold
			if count >= DATA_SET_LOAD_EQUALIZER:
				break
			#Load the actual images and append them to training_data.
			try:
				image_array = cv2.resize(cv2.imread(os.path.join(path, image), cv2.IMREAD_GRAYSCALE), IMAGE_SIZE)
				training_data.append([image_array, class_index])
				count += 1
			except Exception as e:
				pass
	
	#Shuffle the training_data array. 			
	random.shuffle(training_data)

def main():
	create_training_data()
	
	# Since, y is a function of X.
	X = []	# For the data
	y = []	# For the label

	for data, label in training_data:
		X.append(data)
		y.append(np_utils.to_categorical(label, num_classes = len(CLASSES))) 
		#convert the labels to binary to use them with categorical_crossentropy
	X = numpy.array(X).reshape(-1, *IMAGE_SIZE, 1)
	y = numpy.array(y)
	
	#Save the data so you don't have to load it everytime.
	if not (os.path.isdir("pickles")):
		os.mkdir("pickles")		

	pickle_output = open("pickles/X.pickle", "wb")
	pickle.dump(X, pickle_output)
	pickle_output.close()
	
	pickle_output = open("pickles/classes.pickle", "wb")
	pickle.dump(CLASSES, pickle_output)
	pickle_output.close()
	
	pickle_output = open("pickles/y.pickle", "wb")
	pickle.dump(y, pickle_output)
	pickle_output.close()
	
	pickle_output = open("pickles/image_size.pickle", "wb")
	pickle.dump(IMAGE_SIZE, pickle_output)
	pickle_output.close()
	
	print("{} data images loaded successfully.".format(len(X)))
	print("With {} labels: {}".format(len(CLASSES), CLASSES))
	
if __name__ == "__main__":
	main()
