########################################################################
# Project 2 - Physical Reasoning
# Group 6
# Joel, Caitlin & Avinash
########################################################################

import numpy as np
from PIL import Image
import pandas as pd 
import cv2

# read in image png and convert to array map
def loadImage(fileName):
	image = cv2.imread(fileName)
	return image


def blackMask(image):
	lower = np.array([0, 0, 0])
	upper = np.array([15, 15, 15])
	shapeMask = cv2.inRange(image, lower, upper)
	return shapeMask

def blueMask(image):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	lower = np.array([110,50,50])
	upper = np.array([130,255,255])
	shapeMask = cv2.inRange(hsv, lower, upper)
	return shapeMask

def findSupportedPoints(topPixels, bottomPixels):
	supportedPixels = []
	topPixels[topPixels[:,0].argsort()]
	bottomPixels[bottomPixels[:,0].argsort()]
	checkSupportPixels = bottomPixels - [0,1]
	supportedPixels = np.array([x for x in set(tuple(x) for x in checkSupportPixels) & set(tuple(x) for x in topPixels)])
	#supportedPixels = np.intersect1d(checkSupportPixels, topPixels)
	sort = supportedPixels[supportedPixels[:,0].argsort()]
	return sort

def getCenterOfGravity(objectPixels):
	xValues = objectPixels[:,0]
	yValues = objectPixels[:,1]
	maxYIndex = yValues.tolist().index(max(yValues))
	xCenter = xValues[maxYIndex]
	maxXIndex = xValues.tolist().index(max(xValues))
	yCenter = yValues[maxXIndex]
	return [xCenter,yCenter]

def checkCenterOfGravity(objectPixels, supportObjectPixels):
	centerOfGravity = getCenterOfGravity(objectPixels)
	supportedPoints = findSupportedPoints(objectPixels,supportObjectPixels)
	supportedYValues = supportedPoints[:,1]
	if np.isin(centerOfGravity[1], supportedYValues): 
		return True
	else:
		return False

def moveBallByOne(image,ballPixels):
	newImage = image
	for p in ballPixels:
		x = p[0]
		y = p[1]
		newImage[x,y,0] = 255
		newImage[x,y,1] = 255
		newImage[x,y,2] = 255
		newImage[x+1,y+1] = 255
		newImage[x+1,y+1] = 0
		newImage[x+1,y+1] = 0
	return newImage


def rollBall(startingImage):
	image = startingImage
	images = [image]
	bluePixels = cv2.findNonZero(blueMask(startingImage))
	ballPixels = bluePixels[:,0]
	blackPixels = cv2.findNonZero(blackMask(startingImage))
	rampPixels = blackPixels[:,0]
	centerOfGravitySupported = checkCenterOfGravity(ballPixels, rampPixels)
	#while(~centerOfGravitySupported):
	image = moveBallByOne(image, ballPixels)
	cv2.imshow("Mask", image)
	cv2.waitKey(0)





def main():
	image = loadImage('rolling_test.png')
	rollBall(image)
	# find all the 'black' shapes in the image
	#cv2.imshow("Mask", blackShapeMask(image))
	#cv2.waitKey(0)
	# bluePixels = cv2.findNonZero(blueMask(image))
	# bluePixels = bluePixels[:,0]
	# blackPixels = cv2.findNonZero(blackMask(image))
	# blackPixels = blackPixels[:,0]
	# supportedPoints = findSupportedPoints(bluePixels,blackPixels)
	# print(supportedPoints)

	





main()