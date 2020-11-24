

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
sleepTimes = [0.15] * 7
sleepTimes[4] = 0.15
sleepTimes[5] = 0.15

"""
Hardcoded positions of game piece hole references.
"""
refPtLD = (350, 870)
refPtRD = (1650, 870)
refPtLU = (450, 130)
refPtRU = (1550, 110)

"""
Interpolate to get all positions
"""
gamePositions = [[(0,0) for i in range(7)] for j in range(6)]
gameHoleReferences = [[(0,0,0) for i in range(7)] for j in range(6)]
print(gamePositions)

def fillGamePositions():
    gamePositions[0][0] = refPtLU
    gamePositions[0][6] = refPtRU
    gamePositions[5][0] = refPtLD
    gamePositions[5][6] = refPtRD

    for i in range(1,6):
        gamePositions[0][i] = (refPtLU[0] - (refPtLU[0]-refPtRU[0]) * i/6.0, refPtLU[1] - (refPtLU[1]-refPtRU[1]) * i/6.0)
    for i in range(1,6):
        gamePositions[5][i] = (refPtLD[0] - (refPtLD[0]-refPtRD[0]) * i/6.0, refPtLD[1] - (refPtLD[1]-refPtRD[1]) * i/6.0)
    for i in range(7):
        t = gamePositions[0][i]
        b = gamePositions[5][i]
        for j in range(1,5):
            gamePositions[j][i] = (t[0] - (t[0]-b[0]) * j/5.0, t[1] - (t[1]-b[1]) * j/5.0)
    for i in range(6):
        for j in range(7):
            hole = gamePositions[i][j]
            gamePositions[i][j] = (int(hole[0]), int(hole[1]))
    print(gamePositions)
fillGamePositions()


for p in pinNums:
    GPIO.setup(p, GPIO.OUT)
    time.sleep(sleepTime)
    GPIO.output(p, GPIO.HIGH)

def activateSolenoid(solenoid):
    inp = solenoid
    GPIO.output(pinNums[inp%7], GPIO.LOW)
    time.sleep(sleepTimes[inp%7])
    GPIO.output(pinNums[inp % 7], GPIO.HIGH)

def calibrateBoardHoles(img):
    for i in range(6):
        for j in range(7):
            x = gamePositions[i][j][0]
            y = gamePositions[i][j][1]
            print(x,y)

def getBoardState():
    camera.capture('/home/pi/mu_code/Connect4RPiRobot/image.jpg')



camera = PiCamera()
camera.rotation = 180

"""
Primary algorithm pseudo code:

while True:
    take picture
    analyze each relevant hole (7)
        if a hole is yellow 2 shots in a row, update gameboard





"""
camera.start_preview()
sleep(3)
camera.capture('/home/pi/mu_code/Connect4RPiRobot/image.jpg')
camera.stop_preview()
sleep(1)

img = image.imread('/home/pi/mu_code/Connect4RPiRobot/image.jpg')
print(img)
print(len(img))
print(len(img[0]))
print(type(img))
a = np.copy(img)
blockSize = 100
for i in range(6):
    for j in range(7):
        x = gamePositions[i][j][0]
        y = gamePositions[i][j][1]
        print(x,y)
        #a[y - blockSize//2:y + blockSize//2,x - blockSize//2:x + blockSize//2] = [255,255,255]

plt.imshow(a)
plt.show()









