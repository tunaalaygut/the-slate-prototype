#Image that PEGI will predict should be given as an argument.

from tensorflow import keras
import cv2
import numpy
import pickle

pickle_IMAGE_SIZE_file = open("pickles/image_size.pickle", "rb")
pickle_CLASSES_file = open("pickles/classes.pickle", "rb")

IMAGE_SIZE = pickle.load(pickle_IMAGE_SIZE_file)
CLASSES = pickle.load(pickle_CLASSES_file)

pickle_IMAGE_SIZE_file.close()
pickle_CLASSES_file.close()

model = keras.models.load_model("model_output/pegi.h5")
image = cv2.imread("test_images/deneme_2.png", cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image, IMAGE_SIZE)
image = image.astype("float") / 255.0
image = image.reshape((1, image.shape[0], image.shape[1], 1))

prediction = model.predict(image)

index = prediction.argmax(axis=1)[0]
label = CLASSES[index]
percentage = "%{}".format(numpy.amax(prediction) * 100)

print("It is a %%%.2f" % (numpy.amax(prediction) * 100) + " " + label + ".")
print(prediction)
