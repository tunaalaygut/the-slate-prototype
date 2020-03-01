"""
slapi.py: This is the API that handles POST request made to the server. Takes
an image along with the POST request, processes it and returns the
interpretation.
"""

# Imports
import time

from flask import Flask, \
    request,\
    jsonify, \
    abort
import cv2
import numpy
# Main actors
from classifier.model_service import PEGI
from detector.hand_detector import HILMI
from classifier.train.pickle_utility import get_pickle_object
from utils.sampler import get_sample_image

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


# Global variables

# Regarding HILMI
weights_dir = "C:/Users/alaygut/Desktop/the-slate-prototype/" \
              "detector/weights/pegi.weights"
config_dir = "C:/Users/alaygut/Desktop/the-slate-prototype/pegi.cfg"

hilmi = HILMI(weights_dir, config_dir)

# Regarding PEGI
pickle_dir = "C:/Users/alaygut/Desktop/the-slate-prototype/" \
             "classifier/train/pickles"
model_path = "C:/Users/alaygut/Desktop/the-slate-prototype/" \
             "classifier/model_output/pegi.h5"

pegi = PEGI(model_path,
            get_pickle_object(f"{pickle_dir}/image_size.pickle"),
            get_pickle_object(f"{pickle_dir}/classes.pickle"))


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/", methods=['POST'])
def interpret():
    """
    This function is, basically, the door that opens the SLATE project to
    outside world. When a request made to SLATE's root url (unknown, at the
    moment), with an image, this function ties all the functionality of the
    project and returns a .json file containing the interpretation of the
    gesture that it sees in the POSTed frame.

    Returns:

    """

    frame = cv2.imdecode(numpy.fromstring(request.files['frame'].read(),
                                          numpy.uint8),
                         cv2.IMREAD_UNCHANGED)

    indexes, boxes, confidences = hilmi.detect(frame)

    response = []
    responses = []
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            top_left = x, y
            bottom_right = x + w, y + h
            detect_confidence = confidences[i]
            sample = get_sample_image(frame, (top_left, bottom_right))

            # PEGI works here
            label, confidence = pegi.predict(sample)

            responses.append({
                "label": label,
                "x1": top_left[0],
                "y1": top_left[1],
                "x2": bottom_right[0],
                "y2": bottom_right[1],
                "confidence": round(confidence * detect_confidence, 2)
            })
    response.append(responses)

    try:
        return jsonify({"interpretation": responses}), 200
    except FileNotFoundError:
        abort(404)

