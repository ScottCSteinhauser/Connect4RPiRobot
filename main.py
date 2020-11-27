

from picamera import PiCamera
from time import sleep
import numpy as np
from skimage import data
import matplotlib.pyplot as plt
from matplotlib import image
import RPi.GPIO as GPIO
import time
from Connect4Board import *

GPIO.setmode(GPIO.BCM)

pinNums = [7,8,25,24,23,18,15]
sleepTime = 0.15
sleepTimes = [0.17,0.15,0.15,0.15,0.12,0.15,0.15]
lightPin = 16

iterations = 500 # number of monte carlo simulations per move, increases AI difficulty and runtime

"""
Hardcoded positions of game piece hole references.
"""
refPtLD = (400, 950)
refPtRD = (1650, 910)
refPtLU = (435, 130)
refPtRU = (1570, 90)
blockSize = 100

"""
Interpolate to get all positions
"""
gamePositions = [[(0,0) for i in range(7)] for j in range(6)]
gameHoleReferences = [[(0,0,0) for i in range(7)] for j in range(6)]
boardState = [0]*7
prevBoardState1 = [0]*7
prevBoardState2 = [0]*7

for p in pinNums:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, GPIO.HIGH)
    time.sleep(sleepTime)
GPIO.setup(lightPin, GPIO.OUT)
GPIO.output(lightPin, GPIO.LOW)

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




def activateSolenoid(solenoid):
    inp = solenoid
    GPIO.output(pinNums[inp%7], GPIO.LOW)
    time.sleep(sleepTimes[inp%7])
    GPIO.output(pinNums[inp % 7], GPIO.HIGH)

def getBoardHoleValues(img):
    values = [[(0,0,0) for i in range(7)] for j in range(6)]
    for i in range(6):
        for j in range(7):
            x = gamePositions[i][j][0]
            y = gamePositions[i][j][1]
            avgR = np.average(img[y-blockSize//2:y+blockSize//2, x-blockSize//2:x+blockSize//2, 0])
            avgG = np.average(img[y-blockSize//2:y+blockSize//2, x-blockSize//2:x+blockSize//2, 1])
            avgB = np.average(img[y-blockSize//2:y+blockSize//2, x-blockSize//2:x+blockSize//2, 2])
            values[i][j] = (avgR, avgG, avgB)
            #print(x,y,values[i][j])
    return values

def getBoardState(cameraIsOn = True):
    if not cameraIsOn:
        camera.start_preview()
        sleep(2)
    camera.capture('/home/pi/mu_code/Connect4RPiRobot/image.jpg')
    img = image.imread('/home/pi/mu_code/Connect4RPiRobot/image.jpg')
    values = getBoardHoleValues(img)
    differences = [[0 for i in range(7)] for j in range(6)]
    for i in range(6):
        for j in range(7):
            for k in range(3):
                differences[i][j] += abs(values[i][j][k] - gameHoleReferences[i][j][k])**2
    #print(differences)
    curBoardState = [x for x in boardState]
    for i in range(7):
        if curBoardState[i] == 6:
            continue
        if (differences[5-curBoardState[i]][i]) > 400:
            curBoardState[i]+=1
    if not cameraIsOn:
        camera.stop_preview()
    return curBoardState

def processMove(game, move, cameraIsOn = True):
    GPIO.output(lightPin, GPIO.LOW)
    game.makeMove(move)
    counterMove = game.AImakeMove(iterations)
    activateSolenoid(counterMove)
    print(game.boardToString())
    boardState[move]+=1
    boardState[counterMove]+=1
    print(move, counterMove)
    GPIO.output(lightPin, GPIO.HIGH)
    # stretch - add function to detect if move was succesful

def flashLight():
    for i in range(10):
        GPIO.output(lightPin, GPIO.HIGH)
        sleep(0.2)
        GPIO.output(lightPin, GPIO.LOW)
        sleep(0.2)


camera = PiCamera()

"""
Primary algorithm pseudo code:

while True:
    take picture
    analyze each relevant hole (7)
        if a hole is yellow 2 shots in a row, update gameboard





"""
camera.start_preview()
sleep(3)
camera.capture('/home/pi/mu_code/Connect4RPiRobot/imageR.jpg')
img = image.imread('/home/pi/mu_code/Connect4RPiRobot/imageR.jpg')
a = np.copy(img)

gameHoleReferences = getBoardHoleValues(a)


game = Connect4Board()

GPIO.output(lightPin, GPIO.HIGH)

while True:
    inp = "bs"
    if inp == "bs":
        b = getBoardState(True)
        sleep(0.1)
        if b == prevBoardState1 == prevBoardState2 and b != boardState:
            #get action
            action = -1
            for i in range(7):
                if b[i] != boardState[i]:
                    action = i
            processMove(game, action)
            print("Move in", action, "th column detected")
        else:
            prevBoardState2 = [x for x in prevBoardState1]
            prevBoardState1 = [x for x in b]
        print(b)
        print(boardState)
        if game.checkForWin(1):
            print("Player 1 Wins!")
            flashLight()
            break
        elif game.checkForWin(2):
            print("Player 2 Wins!")
            flashLight()
            break

camera.stop_preview()

"""
for i in range(6):
    for j in range(7):
        x = gamePositions[i][j][0]
        y = gamePositions[i][j][1]
        a[y - blockSize//2:y + blockSize//2,x - blockSize//2:x + blockSize//2] = [255,255,255]

plt.imshow(a)
plt.show()
"""
