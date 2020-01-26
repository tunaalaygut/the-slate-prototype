import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Conv2D, MaxPooling2D, Flatten
import pickle
import numpy
import os

pickle_X_file = open("pickles/X.pickle", "rb")
pickle_y_file = open("pickles/y.pickle", "rb")
pickle_CLASSES_file = open("pickles/classes.pickle", "rb")

X = pickle.load(pickle_X_file)
y = pickle.load(pickle_y_file)
CLASSES = pickle.load(pickle_CLASSES_file)

pickle_X_file.close()
pickle_y_file.close()
pickle_CLASSES_file.close()

X = X / 255.0 #Since X is grayscale.

BATCH_SIZE = 32
EPOCHS = 7

model = Sequential()

model.add( Conv2D(32, (3, 3), input_shape = X.shape[1:]) )
model.add( Activation('relu') )
model.add( MaxPooling2D(2, 2) )

model.add( Conv2D(64, (3, 3)) )
model.add( Activation('relu') )
model.add(MaxPooling2D(2, 2))

model.add( Conv2D(128, (3, 3)) )
model.add( Activation('relu') )
model.add(MaxPooling2D(2, 2))

#model.add( Conv2D(128, (3, 3)) )
#model.add( Activation('relu') )
#model.add(MaxPooling2D(2, 2))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))

model.add(Dense(len(CLASSES)))
model.add(Activation('softmax'))

model.compile(loss = "categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

model.fit(X, y, batch_size = BATCH_SIZE, epochs = EPOCHS, validation_split = 0.20)

if not os.path.isdir("model_output"):
	os.mkdir("model_output")
	
model.save("model_output/pegi.h5")
