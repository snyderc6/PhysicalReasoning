from findObjects import *
import cv2
from PIL import Image
from pivot import *


def make_image(black, blue, dimensions):
    im = np.ones((dimensions[0], dimensions[1], 3))
    for o in black:
        for x in range(len(o.image)):
            for y in range(len(o.image[0])):
                if o.image[x][y] != 0:
                    im[x + o.coords[1]][y + o.coords[0]][0] = 0
                    im[x + o.coords[1]][y + o.coords[0]][1] = 0
                    im[x + o.coords[1]][y + o.coords[0]][2] = 0
    for o in blue:
        for x in range(len(o.image)):
            for y in range(len(o.image[0])):
                if (o.image[x][y] != 0) and (x + o.coords[1] < dimensions[0]) and (y + o.coords[0] < dimensions[1]):
                    im[x + o.coords[1]][y + o.coords[0]][0] = 0
                    im[x + o.coords[1]][y + o.coords[0]][1] = 0
                    im[x + o.coords[1]][y + o.coords[0]][2] = 1
    im = Image.fromarray(im.astype('uint8') * 255)
    return im


def move_shapes(black, blue):
    for o in blue:
        vspd = o.area
        if o.pivot != None:
            # print("pivoting")
            new_image, new_rotation = pivot_object(o, o.pivot, [])
            o.image = new_image
            o.rotation = new_rotation
        else:
            o.coords = o.coords[0] + 1 * (vspd > 0), o.coords[1]

        """	
        for o2 in black+blue:
            #do stuff
            i = 0
        """


def run_machine(black, blue, dims=(800, 800)):
    movieImages = [make_image(black, blue, dims), ]
    # im.show()
    i = 0
    while i < 50:
        i += 1
        # check if anything changed since last frame
        move_shapes(black, blue)
        movieImages += [make_image(black, blue, dims), ]
    return movieImages


def main():
    image = cv2.imread("problems/pivot_test.png")
    dims = image.shape
    black, blue, green, yellow = segment_objects(image)
    print(len(black), len(blue), len(green), len(yellow))
    attach_yellows(blue, yellow)
    movie = run_machine(black, blue, dims)
    for i, im in enumerate(movie):
        im.save('out/im-' + str(i) + '.png')
    # imageToShow = segmentblu[0].image
    # Image.fromarray((1-imageToShow)*255).show()
    # print(len(segmentbl), len(segmentblu), len(segmentg), len(segmenty))


main()