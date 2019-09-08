## Simple Motion Detection on Web Browser

### Introduction
The repo is a toy project based on PyImageSearch Blog post [OpenCV Stream Video to Web Browser Html Page](https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/#post_downloads) meant to learn how to perform super simple motion detection against video stream and display result on web browser.

### Setup Virtualenv (macos tested only, linux should work)
This repo uses pipenv to setup virtualenv and manage packages and requires Python 3.6+ 
1. The pipenv installation steps can be found [here](https://github.com/pypa/pipenv)
2. Run `pipenv install` in root dir of this repo to install packages, including `flask`, `opencv`, `imutils`, `numpy`

### Run simple motion detection demo
1. Run `pipenv shell` under root dir of repo to enter virtualenv
2. Run `python webstreaming.py -i 0.0.0.0 -p 8000` to start flask server
3. Visit `http://127.0.0.1:8000` and there will be a live video stream!
![Motion Detector Demo](resources/motion_detection.png)

4. Press `Ctrl C` to stop the demo

### Steps of simple motion detection
The approach of motion detection in this repo is the very simple one. It consists three steps basically.

#### 1. Accumulate background image
The first step is to collect the background, for example like below, three raw images captured by camera is accumulated averaged using `cv2.accumulateWeighted` to get the basic background image.
![Accumulated Background Image](resources/accumulated_bg_generation.png)

#### 2. Detect edges of moving object
The steps of detecting edges of moving object is:
 
a). The difference between background image and newly captured image is calculated using `cv2.absdiff`

b). Threshold method is performed to distinguish the static background pixels and moving object pixels using `cv2.threshold`

c). Basic edge detection method is used to detect edges of moving objects using `cv2.erode` & `cv2.dilate`

Below is the example of detecting edges of moving object
![Detect edges of moving object](resources/motion_detection_steps_demo.png)

#### 3. Find coordinates of detected objects
At last, `cv2.findContours` is used to find the contour of moving object and then coordinates of objects is calculated. 
