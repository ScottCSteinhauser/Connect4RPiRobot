
from picamera import PiCamera
from time import sleep
import numpy as np
from skimage import data
import matplotlib.pyplot as plt
from matplotlib import image
import RPi.GPIO as GPIO
import time


camera = PiCamera()
camera.start_preview()
sleep(10)
camera.capture('/home/pi/mu_code/Connect4RPiRobot/imageR.jpg')
camera.stop_preview()
sleep(1)
img = image.imread('/home/pi/mu_code/Connect4RPiRobot/imageR.jpg')
a = np.copy(img)