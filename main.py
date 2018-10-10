from findObjects import *
from rolling import *
import cv2
from PIL import Image

def make_image(black,blue):
	im = np.ones((800,800,3))
	for o in black:
		pixels = o.getWorldPixelCoordList()
		for pixel in pixels:
			im[pixel[0]][pixel[1]] = [0,0,0]
	for o in blue:
		pixels = o.getWorldPixelCoordList()
		for pixel in pixels:
			im[pixel[0]][pixel[1]] = [0,0,1]
	im = Image.fromarray(im.astype('uint8')*255)
	return im

def move_shapes(black,blue):
	for o in blue:
		vspd = o.area
		if o.pivot != None:
			#do stuff
			i = 0
		'''for o2 in black+blue:
			if(is_touching(o,o2)) & (~is_supported(o,o2)): 
				#only roll o if touching o2 & not supported
				#roll(o2)
				i = 0'''

		o.coords = o.coords[0]+1*(vspd>0),o.coords[1]

def run_machine(black,blue):
	movieImages = [make_image(black,blue),]
	#im.show()
	i=0
	while i<10:
		i+=1
		black[0].rotation += 1
		#check if anything changed since last frame
		move_shapes(black,blue)
		movieImages += [make_image(black,blue),]
	return movieImages


def main():
    image = cv2.imread("problems/rolling_test.png")
    black,blue, green, yellow = segment_objects(image)
    print(len(black),len(blue),len(green),len(yellow))
    attach_yellows(blue,yellow)
    '''
    blueO = blue[0]
    blackO = black[0]

    touchingVal, orientationVal = is_touching(blueO, blackO)
    print(touchingVal)
    print(orientationVal)
    im = make_image(black, blue)
    im.show()'''

    movie = run_machine(black,blue)
    for i,im in enumerate(movie):
    	im.save('out/im-'+str(i)+'.png')
    #imageToShow = segmentblu[0].image
    #Image.fromarray((1-imageToShow)*255).show()
    #print(len(segmentbl), len(segmentblu), len(segmentg), len(segmenty))
    



main()