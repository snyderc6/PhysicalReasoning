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

problems = load_images()
print(len(problems))

image = np.array(problems[1])
print(image[20])
#change X color to black in new image
blue = 255
blueImage = np.equal(np.ones(image.shape)*blue,image)*1

print(blueImage[20])

objects = find_all_sub_objects(blueImage,0)
print(len(objects))
#print(objects)