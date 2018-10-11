from findObjects import *
from rolling import *
import cv2
from pivot import *
from PIL import Image
import copy

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
	objectMoved = False
	for o in blue:
		if o.pivot != None:
			new_image, new_rotation = pivot_object(o, o.pivot, [])
			# if pivot_moved == True:
			# 	objectMoved = True
			o.image = new_image
			o.rotation = new_rotation
		touching_o = []
		supported_underneath = False
		direction_to_move = ["down"]
		#blue.remove(o)#remove o from list
		print(len(black+blue))
		obj_list = copy.copy(black+blue)
		obj_list.remove(o)
		for o2 in obj_list:
			touching,direction = is_touching(o,o2)
			if(touching & ("above" in direction)): 
				direction.remove("above")
				direction.append("down")
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
		if not supported_underneath:
			if(o.ropeIds != None):
				#check if supported by string do something
				i = 0
			if 'down' in direction_to_move:
				print('moving down')
				objectMoved = True
				o.coords = [o.coords[0]+1,o.coords[1]]
			if 'left_of' in direction_to_move:
				print('moving left')
				objectMoved = True
				o.coords = [o.coords[0],o.coords[1]-1]
			if 'right_of' in direction_to_move:	
				print('moving right')
				objectMoved = True
				o.coords = [o.coords[0],o.coords[1]+1]
	return objectMoved

def run_machine(black,blue):
	someObjectsMoved = True
	movieImages = [make_image(black,blue),]
	i=0
	#while someObjectsMoved:
	while i < 8:
		i+=1
		print('Step '+str(i))
		#black[0].rotation += 1
		#check if anything changed since last frame
		someObjectsMoved = move_shapes(black,blue)
		movieImages += [make_image(black,blue),]
	return movieImages

def make_video(image1, images):
	height, width, layers = np.asarray(images[0]).shape

	video = cv2.VideoWriter("video.avi", -1, 1, (width,height))

	for image in images:
  		video.write(np.asarray(image))

	cv2.destroyAllWindows()
	video.release()


def main():
	image = cv2.imread("problems/6-1-small.png")
	black,blue, green, yellow = segment_objects(image)
	#print(blue)
	print(len(black),len(blue),len(green),len(yellow))
	attach_yellows(blue,yellow)
	attach_greens(blue,green)
    # blueO = blue[0]
    # blackO = black[0]
    # touchingVal, orientationVal = is_touching(blueO, blackO)
    # print(orientationVal)
    #move_shapes(blue,black)
    # im = make_image(black, blue)
    # im.show()
	movie = run_machine(black,blue)
	for i,im in enumerate(movie):
		im.save('out/im-'+str(i)+'.png')
	make_video(image,movie)
    #imageToShow = segmentblu[0].image
    #Image.fromarray((1-imageToShow)*255).show()
    #print(len(segmentbl), len(segmentblu), len(segmentg), len(segmenty))
    



main()