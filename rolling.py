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
	checkSupportPixels = bottomPixels + [0,2]
	supportedPixels = np.array([x for x in set(tuple(x) for x in checkSupportPixels) & set(tuple(x) for x in topPixels)])
	#supportedPixels = np.intersect1d(checkSupportPixels, topPixels)
	return supportedPixels
	



def main():
	image = loadImage('rolling_test.png')
	# find all the 'black' shapes in the image
	#cv2.imshow("Mask", blackShapeMask(image))
	#cv2.waitKey(0)
	bluePixels = cv2.findNonZero(blueMask(image))
	bluePixels = bluePixels[:,0]
	blackPixels = cv2.findNonZero(blackMask(image))
	blackPixels = blackPixels[:,0]
	blackPixels[blackPixels[:,1].argsort()]
	bluePixels[bluePixels[:,1].argsort()]
	print(bluePixels[0:100])
	print("b")
	print(blackPixels[0:100])
	#supportedPoints = findSupportedPoints(bluePixels,blackPixels)
	#print(supportedPoints)
	





main()