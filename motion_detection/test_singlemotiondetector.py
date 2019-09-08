import os
import unittest

import cv2
import imutils
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from motion_detection.singlemotiondetector import SingleMotionDetector

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), 'resources')


class SingleMotionDetectorTest(unittest.TestCase):
    def test_should_weighted_accumulate_images(self):
        motion_detector = SingleMotionDetector()

        imgs = []

        for i in range(4):
            img_path = os.path.join(RESOURCES_DIR, 'captured_images_{}.png'.format(i + 1))
            img = cv2.imread(img_path)
            imgs.append(img)

        img_1 = self.gray_and_gaussian_blur_img(imgs[0])
        img_2 = self.gray_and_gaussian_blur_img(imgs[1])
        img_3 = self.gray_and_gaussian_blur_img(imgs[2])

        motion_detector.update(img_1)
        motion_detector.update(img_2)
        motion_detector.update(img_3)

        figure: Figure = plt.figure()

        axes_img_1: Axes = figure.add_subplot(221)
        axes_img_1.imshow(img_1)
        axes_img_1.set_title('grayed img 1')

        axes_img_2: Axes = figure.add_subplot(222)
        axes_img_2.imshow(img_2)
        axes_img_2.set_title('grayed img 2')

        axes_img_3: Axes = figure.add_subplot(223)
        axes_img_3.imshow(img_3)
        axes_img_3.set_title('grayed img 3')

        axes_img_4: Axes = figure.add_subplot(224)
        axes_img_4.imshow(motion_detector.bg)
        axes_img_4.set_title('accumulated bg')

        plt.show()


    def test_should_detect_moving_object(self):
        motion_detector = SingleMotionDetector()

        imgs = []

        for i in range(4):
            img_path = os.path.join(RESOURCES_DIR, 'captured_images_{}.png'.format(i + 1))
            img = cv2.imread(img_path)
            imgs.append(img)

        motion_detector.update(self.gray_and_gaussian_blur_img(imgs[0]))
        motion_detector.update(self.gray_and_gaussian_blur_img(imgs[1]))
        motion_detector.update(self.gray_and_gaussian_blur_img(imgs[2]))
        last_gray_img = self.gray_and_gaussian_blur_img(imgs[3])

        delta = cv2.absdiff(motion_detector.bg.astype("uint8"), last_gray_img)

        _, thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)

        thresh_erode = cv2.erode(thresh, None, iterations=2)
        thresh_erode_dilate = cv2.dilate(thresh_erode, None, iterations=2)

        figure: Figure = plt.figure()
        axes_bg_img: Axes = figure.add_subplot(231)
        axes_bg_img.imshow(motion_detector.bg)
        axes_bg_img.set_title('1. accumulated back ground')

        axes_last_img: Axes = figure.add_subplot(232)
        axes_last_img.imshow(last_gray_img)
        axes_last_img.set_title('2. latest image')

        axes_diff: Axes = figure.add_subplot(233)
        axes_diff.imshow(delta)
        axes_diff.set_title('3. difference between bg and latest image')

        axes_thresh: Axes = figure.add_subplot(234)
        axes_thresh.imshow(thresh)
        axes_thresh.set_title('4. threshold on diff img')

        axes_thresh_erode: Axes = figure.add_subplot(235)
        axes_thresh_erode.imshow(thresh_erode)
        axes_thresh_erode.set_title('5. erode threshold')

        axes_thresh_erode_dilate: Axes = figure.add_subplot(236)
        axes_thresh_erode_dilate.imshow(thresh_erode_dilate)
        axes_thresh_erode_dilate.set_title('6. dilate on eroded threshold')

        plt.show()

    def gray_and_gaussian_blur_img(self, img):
        img = imutils.resize(img, width=400)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        return gray


# This can be used to capture images from camera using cv2
def capture_photos():
    import cv2

    camera = cv2.VideoCapture(0)
    for i in range(5):
        return_value, image = camera.read()
        cv2.imwrite(os.path.join(RESOURCES_DIR, 'captured_images_{}.png'.format(i)), image)
    del (camera)
