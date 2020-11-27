
from picamera import PiCamera
from time import sleep
import numpy as np
from skimage import data
import matplotlib.pyplot as plt
from matplotlib import image
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pinNums = [15,18,23,24,25,8,7]
sleepTime = 0.15
sleepTimes = [0.15,0.15,0.12,0.15,0.15,0.15,0.15]


for p in pinNums:
    GPIO.setup(p, GPIO.OUT)
    time.sleep(sleepTime)
    GPIO.output(p, GPIO.HIGH)

"""
for i in range(8):
    GPIO.output(pinNums[(i-1)%8], GPIO.HIGH)
    GPIO.output(pinNums[i%8], GPIO.LOW)
    time.sleep(sleepTime)
GPIO.output(pinNums[-1], GPIO.HIGH)
"""

while True:
    inp = input("Take input: ")
    if inp == "done":
        break
    elif inp == "all":
        for p in pinNums:
            GPIO.output(p, GPIO.LOW)
            time.sleep(sleepTime)
            GPIO.output(p, GPIO.HIGH)
        continue
    inp = int(inp)
    GPIO.output(pinNums[inp%7], GPIO.LOW)
    time.sleep(sleepTimes[inp%7])
    GPIO.output(pinNums[inp % 7], GPIO.HIGH)



GPIO.cleanup()


""" -- Camera Code

camera = PiCamera()

camera.start_preview()
sleep(3)
camera.capture('/home/pi/mu_code/Connect4/image.jpg')
camera.stop_preview()
sleep(1)
img = image.imread('/home/pi/mu_code/Connect4/image.jpg')
print(img)
type(img)


plt.imshow(img)
plt.show()

"""