# The SLATE Neural Engine (SNE)
The SLATE Neural Engine (SNE) is a component of the SLATE project. The S.L.A.T.E. (short for Sign Language &amp; Audio Transcriber Enclosure) is a product that is designed for speech/hearing impaired to facilitate their daily communications. Project aims to provide a solution by translating sign language gestures to plain text.

SNE is the part of the SLATE project that does the actual sign language-to-text translation.
To get the SNE up and running, (in a Windows 10 environment) the following procedure needs to be followed.

## Installation
To run the SNE you need a python virtual environment. An **Anaconda Virtual Environment** is recommended.

### Installing Anaconda and Setting up the Environment
Go to [official Anaconda web site](https://www.anaconda.com/distribution/) and download Anaconda 2020.02 Python 3.7 version.

Once you downloaded and installed Anaconda open the **Anaconda Prompt** (open as Administrator to avoid any privilege problem) and type:
```
conda create -n sne python=3.7
```
This command creates a new Anaconda environment with Python 3.7 (newer versions of Python does not support Tensorflow 2.x at the moment)
To start working in the envrionment that was just created type the command
```
conda activate sne
```

 ### Installing Dependencies
To install the dependencies to the virtual environment
```
pip install tensorflow
pip install keras
pip install flask
pip install flask_cors
```

### Installing OpenCV 4.2.0
To make OpenCV work (the way it intended to), it should be built from the source with CUDA (with cuDNN) support. Note that installing the opencv-python with pip will **not** be sufficient.    
To build OpenCV from the source

1. Download OpenCV source code from [this](https://github.com/opencv/opencv/archive/4.2.0.zip) link.
2. Download OpenCV-contrib source code from [this](https://github.com/opencv/opencv_contrib/archive/4.2.0.zip) link.
3. Build the source code. (CMake and Visual Studio can be used.)
4. Once the build is done check the OpenCV installation.

To check
```console
sne@sne:~$ python
>>> import cv2
>>> cv2.__version__
'4.2.0'
```
If the correct version (4.2.0) is displayed, it is done.

### Getting the SNE
Now that the virtual environment is all set up, get the SNE code
```
git clone https://github.com/tunaalaygut/the-slate-prototype.git
```

## Run
After the SNE code is cloned from the repository, cd to the directory and type the following commands to run the engine
```
set FLASK_APP=slapi/slapi
flask run
```
SNE should be started running in localhost:5000.
