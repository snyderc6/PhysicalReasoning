import numpy as np
from copy import deepcopy
from PIL import Image
import os

def load_images(dir = None):
    """
    if no dir specified, take default
    if no problem names are specified, take all in the current dir

    return problems list: 0-4 are options, 5-6 are pictures in a,b, 7 is the question pic
    :param dir:
    :return:
    """
    if dir is None:
        dir = os.path.join(os.getcwd(),'problems')
    problems = []
    problemNames = next(os.walk(dir))[1]
    for f in sorted(os.listdir(dir)):
        im = Image.open(os.path.join(dir, f))
        problems += [im.convert(mode='L'), ]
    return problems


def floodfill(x, y, color, old_matrix, new_matrix):
    # assume surface is a 2D image and surface[x][y] is the color at x, y.
    # this avoids the stack overflow
    theStack = [(x, y)]

    width = len(old_matrix)
    height = len(old_matrix[0])
    while len(theStack) > 0:
        x, y = theStack.pop()
        if old_matrix[x][y] != color:
            continue
        new_matrix[x][y] = color
        old_matrix[x][y] = 1 - color
        if x < width - 1:
            theStack.append((x + 1, y))  # right
        if x > 0:
            theStack.append((x - 1, y))  # left
        if y < height - 1:
            theStack.append((x, y + 1))  # down
        if y > 0:
            theStack.append((x, y - 1))  # up

def find_available(matrix, val: int):
    """
    Find the available locations of the val value, if not found, return False
    :param matrix:
    :param val:
    :return:
    """
    loc = np.nonzero(matrix == val)
    if list(loc[0]) == []:
        return False
    else:
        return loc

def find_all_sub_objects(matrix, val, color=0):
    """
    Find all the sub objects in the matrix using floodfill algorithm
    :param matrix: binary ndarray representation for image
    :param val: the value to search for (in the case of image inversion, val is used instead)
    :return:
    """
    #matrix = matrix[1:-1,1:-1]
    objects = []
    ob_matrix = deepcopy(matrix)
    avail_loc = find_available(matrix, val=val)
    while avail_loc:
        next_avail_loc = avail_loc[0][0], avail_loc[1][0]
        if val == 1:
            new_matrix = np.zeros(ob_matrix.shape)
        elif val == 0:
            new_matrix = np.ones(ob_matrix.shape)
        floodfill(x=next_avail_loc[0], y=next_avail_loc[1], color=color, old_matrix=ob_matrix, new_matrix=new_matrix)
        objects.append(new_matrix)
        avail_loc = find_available(ob_matrix, val=val)
    return objects

from PIL import Image
import copy
from SolidObject import *
import cv2
import math


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

def yellowMask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([20,50,50])
    upper = np.array([40,255,255])
    shapeMask = cv2.inRange(hsv, lower, upper)
    return shapeMask

def greenMask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([40,50,50])
    upper = np.array([80,255,255])
    shapeMask = cv2.inRange(hsv, lower, upper)
    return shapeMask

def image_to_segimage(image):

    #todo: get pivots and ropes here too 
    return blueMask(image), blackMask(image), yellowMask(image), greenMask(image)


def segment_objects(image):
    #problems = load_images()
    im = np.array(Image.fromarray(image).convert('HSV'))
    #image = np.array(problems[1])[0:50,0:60]
    im2 = np.array(image)
    #convert image to custom discrete colors

    objectGroups = []
    for colorImage in image_to_segimage(image): #blue, black
        #colorImage = copy.copy(image)
        #colorImage[image!=color] = 255
        #colorImage[image==color] = 0
        #ci = 1-colorImage
        #Image.fromarray(255-colorImage).show()
        #display(Image.fromarray(image))
        #display(Image.fromarray(colorImage))
        objectGroups += [find_all_sub_objects(1-colorImage/255,0),]

    for group in objectGroups:
        for i,o in enumerate(group):
            o = 1-o
            im = Image.fromarray(o*255).convert('L')
            bbox = im.getbbox()
            coords = (bbox[1],bbox[0])
            im = im.crop(bbox)
            
            group[i] = [np.array(im)/255,coords]
            #display(im)

    blueObjects = [SolidObject(x[0],x[1],isBlue=True) for x in objectGroups[0]]
    blackObjects = [SolidObject(x[0],x[1]) for x in objectGroups[1]]
    y = [SolidObject(x[0],x[1]) for x in objectGroups[2]]
    g = [SolidObject(x[0],x[1]) for x in objectGroups[3]]
    return blackObjects,blueObjects,g,y

def point_distance(x,y,x2,y2):
    return math.sqrt((x-x2)*(x-x2)+(y-y2)*(y-y2))

def attach_yellows(blues,yellows):
    for yellow in yellows:
        closestdist = 10000
        closest = None
        ycoords = yellow.coords[0]+yellow.center[0],yellow.coords[1]+yellow.center[1]
        for o in blues:
            coords = o.coords[0]+o.center[0],o.coords[1]+o.center[1],
            if point_distance(*coords,*ycoords) < closestdist:
                closest = o
                closestdist = point_distance(*coords,*ycoords)
        closest.pivot = ycoords[0]-(closest.coords[0]),ycoords[1]-(closest.coords[1])
        print('attached pivot at',closest.pivot)

def attach_greens(blues,greens):
    for green in greens:
        furthest_point1 = None
        fDist = 0
        for point in green.allpixels:
            dist = point_distance(*green.center,*point)
            if dist > fDist:
                fDist = dist
                furthest_point1 = point

        furthest_point2 = None
        fDist = 0
        for point in green.allpixels:
            dist = point_distance(*furthest_point1,*point)
            if dist > fDist:
                fDist = dist
                furthest_point2 = point

        print('green: ',furthest_point1,furthest_point2,green.center)

        prev = None
        for p in [furthest_point1,furthest_point2]:
            closestdist = 10000
            closest = None
            ycoords = green.coords[0]+p[0],green.coords[1]+p[1]
            lst = copy.copy(blues)
            if prev in lst:
                lst.remove(prev)
            for o in lst:
                clist = o.getWorldPixelCoordList()
                for coords in clist:
                    if point_distance(*coords,*ycoords) < closestdist:
                        closest = o
                        closestdist = point_distance(*coords,*ycoords)
            prev = closest
            closest.ropeAttachPoints += [ycoords[0]-(closest.coords[0]),ycoords[1]-(closest.coords[1]),]
            closest.ropeIds += [green,]
            green.ropeIds += [closest,]
            print('attached rope to',closest,'at',closest.ropeAttachPoints)