"""
video_framer.py: This modules is used to save frames of a video file. All the
frames in a video file can be saved to disk. If desired, certain number of
frames can be skipped to increase variety and lower the amount of similar
frames.
"""

# Imports
import argparse
import cv2
import os

# Information
__author__ = "Tuna ALAYGUT"
__copyright__ = "Copyright 2020, The Slate Project"
__status__ = "Development"
__email__ = "alaygut@gmail.com"

# Global variables
parser = argparse.ArgumentParser(description="")
parser.add_argument('-v', '--video', required=True,
                    help="Video file to work with.")
parser.add_argument('-o', '--path', required=True,
                    help="Output path of the snapped images.")
parser.add_argument('-n', '--filename', required=True,
                    help="Filename to save the frames with.")
parser.add_argument('-ext', '--extension', default="png",
                    help="Extension of the saved frames.")
parser.add_argument('-s', '--skip', default=0, type=int,
                    help="Skip this amount of frames.")
args = vars(parser.parse_args())

video = cv2.VideoCapture(args["video"])
output_path = args["path"]
filename = args["filename"]
extension = args["extension"]
skip = args["skip"]

# Create the output path if it does not exist.
if not os.path.isdir(output_path):
    os.makedirs(output_path)


def main():
    print("Video Framer is now working.")
    count = 0
    skip_counter = 0

    while True:
        # Read a frame from the video.
        ret, frame = video.read()

        if ret:
            if skip_counter == skip:
                # Save the frame to the disk.
                temp_filename = f"{output_path}/{filename}_{count}.{extension}"
                cv2.imwrite(temp_filename, cv2.rotate(frame,
                                                      cv2.ROTATE_90_CLOCKWISE))
                print(f"Image {temp_filename} is saved.")

                count += 1
                skip_counter = 0
            else:
                skip_counter += 1
        else:
            break

    print("Video is framed.")
    video.release()


if __name__ == "__main__":
    main()
