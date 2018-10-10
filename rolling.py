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
# def loadImage(fileName):
# 	image = cv2.imread(fileName)
# 	return image


# def blackMask(image):
# 	lower = np.array([0, 0, 0])
# 	upper = np.array([15, 15, 15])
# 	shapeMask = cv2.inRange(image, lower, upper)
# 	return shapeMask

# def blueMask(image):
# 	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# 	lower = np.array([110,50,50])
# 	upper = np.array([130,255,255])
# 	shapeMask = cv2.inRange(hsv, lower, upper)
# 	return shapeMask

def findSupportedPoints(topPixels, bottomPixels):
	supportedPixels = []
	topPixels[topPixels[:,0].argsort()]
	bottomPixels[bottomPixels[:,0].argsort()]
	checkSupportPixels = bottomPixels - [0,1]
	supportedPixels = np.array([x for x in set(tuple(x) for x in checkSupportPixels) & set(tuple(x) for x in topPixels)])
	#supportedPixels = np.intersect1d(checkSupportPixels, topPixels)
	sort = supportedPixels[supportedPixels[:,0].argsort()]
	return sort

def getCenter(objectPixels):
	xValues = objectPixels[:,0]
	yValues = objectPixels[:,1]
	maxYIndex = yValues.tolist().index(max(yValues))
	xCenter = xValues[maxYIndex]
	maxXIndex = xValues.tolist().index(max(xValues))
	yCenter = yValues[maxXIndex]
	return [xCenter,yCenter]

def checkIfSupported(objectPixels, supportObjectPixels):
	centerOfGravity = getCenter(objectPixels)
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
		newImage[x,y,:] = [255,255,255]
		newImage[x+1,y+1,0] = 255
		newImage[x+1,y+1,1] = 0
		newImage[x+1,y+1,2] = 0
	cv2.imshow("image", newImage)
	return newImage


def rollBall(startingImage):
	image = startingImage
	images = [image]
	bluePixels = cv2.findNonZero(blueMask(startingImage))
	ballPixels = bluePixels[:,0]
	print(ballPixels)
	blackPixels = cv2.findNonZero(blackMask(startingImage))
	rampPixels = blackPixels[:,0]
	count = 0
	centerOfGravitySupported = checkIfSupported(ballPixels, rampPixels)
	#while(~centerOfGravitySupported):
	while(count < 4):
		image = moveBallByOne(image, ballPixels)
		images.append(image)
	cv2.imshow("im", image)
	cv2.waitKey(0)

def is_offset(o1_pixels, o2_pixels, offset_val):
	offset_pixels = o1_pixels + offset_val
	shared_pixels = np.array([x for x in set(tuple(x) for x in offset_pixels) & set(tuple(x) for x in o2_pixels)])
	if(len(shared_pixels) > 0):
		return True
	return False

def get_orientation(object1, object2):
	orientation = []
	o1_pixels = object1.allpixels + object1.coords
	o2_pixels = object2.allpixels + object2.coords

	# is_underneath = is_offset(o1_pixels, o2_pixels, [0,-1])
	# if(is_underneath):
	# 	orientation.append("underneath")

	# is_above = is_offset(o1_pixels, o2_pixels, [0,1])
	# if(is_above):
	# 	orientation.append("above")

	# is_right_of = is_offset(o1_pixels, o2_pixels, [-1,0])
	# if(is_right_of):
	# 	orientation.append("right_of")

	is_left_of = is_offset(o1_pixels, o2_pixels, [1,0])
	if(is_left_of):
		orientation.append("left_of")
	
	return orientation

def is_touching(object1, object2):
	orientation = get_orientation(object1, object2)
	if(len(orientation)!=0):
		return True,orientation
	return False,orientation

#def is_supported(object, all_touching_objects):


#def roll(blueObject,blackObject):





# def main():
# 	image = loadImage('rolling_test.png')
# 	rollBall(image)
	# find all the 'black' shapes in the image
	#cv2.imshow("Mask", blackShapeMask(image))
	#cv2.waitKey(0)
	# bluePixels = cv2.findNonZero(blueMask(image))
	# bluePixels = bluePixels[:,0]
	# blackPixels = cv2.findNonZero(blackMask(image))
	# blackPixels = blackPixels[:,0]
	# supportedPoints = findSupportedPoints(bluePixels,blackPixels)
	# print(supportedPoints)

	



