from findObjects import *
from rolling import *
import cv2
from pivot import *
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
		if o.pivot is not None:
			new_image, new_rotation = pivot_object(o, o.pivot, [])
			o.image = new_image
			o.rotation = new_rotation
		touching_o = []
		supported_underneath = False
		direction_to_move = ["down"]
		blue.remove(o)#remove o from list
		for o2 in black+blue:
			touching,direction = is_touching(o,o2)

			if(touching & ("above" in direction)): 
				direction.remove("above")
				touching_o.append([o2,direction])
		for support in touching_o:
			print(support)
			if(is_supported(o, support[0])):
				supported_underneath = True
			else:
				print(support)
				direction_to_move = support[1]
		print("supported",supported_underneath)
		print("dir", direction_to_move)
		if(~supported_underneath):
			if(o.ropeIds != None):
				#check if supported by string do something
				i = 0
			else:
				if direction_to_move[0] == "down":
					o.coords = o.coords[0]+1*(vspd>0),o.coords[1]
				elif direction_to_move[0] == "left_of":
					o.coords = o.coords[0]+1*(vspd>0),o.coords[1]+1*(vspd>0)
				else:	
					o.coords = o.coords[0]+1*(vspd>0),o.coords[1]-1*(vspd>0)


def run_machine(black,blue):
	movieImages = [make_image(black,blue),]
	#im.show()
	i=0
	while i<10:
		i+=1
		print('Step '+str(i))
		black[0].rotation += 1
		#check if anything changed since last frame
		move_shapes(black,blue)
		movieImages += [make_image(black,blue),]
	return movieImages


def main():
    image = cv2.imread("problems/rolling_test.png")
    black,blue, green, yellow = segment_objects(image)
    print(blue)
    print(len(black),len(blue),len(green),len(yellow))
    attach_yellows(blue,yellow)
    blueO = blue[0]
    blackO = black[0]
    # touchingVal, orientationVal = is_touching(blueO, blackO)
    # #print(orientationVal)
    move_shapes(blue,black)
    # im = make_image(black, blue)
    # im.show()

    # movie = run_machine(black,blue)
    # for i,im in enumerate(movie):
    # 	im.save('out/im-'+str(i)+'.png')
    #imageToShow = segmentblu[0].image
    #Image.fromarray((1-imageToShow)*255).show()
    #print(len(segmentbl), len(segmentblu), len(segmentg), len(segmenty))
    



main()