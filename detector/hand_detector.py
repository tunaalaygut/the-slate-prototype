"""
hand_detector.py: This module is used to detects hands in a given frame and
return the positions related to the detected hands.
"""

# Imports
from cv2 import dnn

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"


class HandDetector:
    """
    Initialize an instance of this class by giving a (pre-trained) weights file
    and a config file. Then, you can call the detect function to make
    detections on the frame. A detection confidence can be specified.
    """
    def __init__(self, weights, config, confidence=0.5):
        self.network = dnn.readNet(weights, config)
        layer_names = self.network.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1]
                              for i in self.network.getUnconnectedOutLayers()]
        self.confidence = confidence

    def detect(self, image):
        """

        Args:
            image: image/frame to make the detections on.

        Returns:
            indexes: indexes of the detected hands. (In order to provide
            multiple hand detections.)
            boxes: location(s) of the hand(s) in the frame.
        """
        # ref: https://github.com/darshanadakane/yolov3_objectdetection
        height, width, _ = image.shape
        blob = dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0),
                                 True, crop=False)
        self.network.setInput(blob)
        outs = self.network.forward(self.output_layers)

        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                confidence = scores[0]

                # Hand detected.
                if confidence > self.confidence:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))

        indexes = dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

        return indexes, boxes


def main():
    print("Hello, world!")


if __name__ == "__main__":
    main()
