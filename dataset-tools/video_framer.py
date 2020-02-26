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
parser.add_argument('-ext', '--extension', default="jpg",
                    help="Extension of the saved frames.")
parser.add_argument('-s', '--skip', default=0, type=int,
                    help="Skip this amount of frames.")
parser.add_argument('-sc', '--startcount', default=0, type=int,
                    help="Start counting the frames from this number.")
parser.add_argument('-r', '--resize', default=0, type=int,
                    help="1 to resize the images. Size reduction purposes.")
parser.add_argument('-rf', '--resizefactor', default=50, type=int,
                    help="Size reduction percentage.")
args = vars(parser.parse_args())

video = cv2.VideoCapture(args["video"])
output_path = args["path"]
filename = args["filename"]
extension = args["extension"]
skip = args["skip"]
count = args["startcount"]
resize = bool(args["resize"])
resize_factor = args["resizefactor"]

# Create the output path if it does not exist.
if not os.path.isdir(output_path):
    os.makedirs(output_path)


def main():
    global count

    print("Video Framer is now working.")
    skip_counter = 0

    while True:
        # Read a frame from the video.
        ret, frame = video.read()

        if ret:  # A frame is read.
            if skip_counter == skip:
                # Create the filename.
                temp_filename = f"{output_path}/{filename}_{count}.{extension}"

                # Resize option is turned on.
                if resize:
                    scale = resize_factor / 100
                    height, width, _ = frame.shape
                    frame = cv2.resize(frame,
                                       (int(width*scale), int(height*scale)),
                                       interpolation=cv2.INTER_AREA)
                # Save the image.
                # Depending on image's orientation, you can cv2.rotate the
                # frame.
                cv2.imwrite(temp_filename, frame)
                # Print info message.
                print(f"Image {temp_filename} is saved.")

                count += 1
                skip_counter = 0  # Restart the skip counter.
            else:
                skip_counter += 1
        else:
            break

    print("Video is framed.")
    video.release()


if __name__ == "__main__":
    main()
