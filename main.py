from findObjects import *
from rolling import *
import cv2
from pivot import *
from PIL import Image
import copy

def make_image(black,blue,green,imageSize):
	im = np.ones(imageSize)
	for o in black:
		pixels = o.getWorldPixelCoordList()
		for pixel in pixels:
			if -1 < pixel[0] < imageSize[0] and -1 < pixel[1] < imageSize[1]:
				im[pixel[0]][pixel[1]] = [0,0,0]
	for o in blue:
		pixels = o.getWorldPixelCoordList()
		for pixel in pixels:
			if -1 < pixel[0] < imageSize[0] and -1 < pixel[1] < imageSize[1]:
				im[pixel[0]][pixel[1]] = [1,0,0]
	for o in green:
		pixels = o.getWorldPixelCoordList()
		for pixel in pixels:
			if -1 < pixel[0] < imageSize[0] and -1 < pixel[1] < imageSize[1]:
				im[pixel[0]][pixel[1]] = [0,1,0]
	im = Image.fromarray(im.astype('uint8')*255)
	return im

def move(o, direction_to_move):
	objectMoved = False
	if 'down' in direction_to_move:
		print('moving down')
		objectMoved = True
		o.coords = [o.coords[0]+1,o.coords[1]]
	if 'left_of' in direction_to_move:
		print('moving left')
		objectMoved = True
		o.rotation += 1
		o.coords = [o.coords[0],o.coords[1]-1]
	if 'right_of' in direction_to_move:	
		print('moving right')
		objectMoved = True
		o.rotation -= 1
		o.coords = [o.coords[0],o.coords[1]+1]
	return objectMoved

def move_shapes(black,blue):
	objectsMoved = []
	for o in blue:
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
				#direction.append("down")
				touching_o.append([o2,direction])
		for support in touching_o:
			print(support)
			#if(is_supported_by(o, support[0])):
			if 'underneath' in support[1]:
				supported_underneath = True
				direction_to_move.remove("down")
			else:
				direction_to_move = support[1]
		print("supported",supported_underneath)
		print("dir", direction_to_move)
		if not supported_underneath and not o.pivot:
			objectMoved = move(o, direction_to_move)
			if objectMoved:
				objectsMoved.append(o)
				#move rope(s)
				for rope in o.ropeIds:
					move(rope, direction_to_move)
				#move attached object(s)
				for obj_attached in o.attachedObjects:
					if not obj_attached.pivot:
						move(obj_attached, direction_to_move)
						#try pushing it

		if o.pivot:
			link_objs = o.attachedObjects
			non_supported_link_objs = []
			for obj in link_objs:
				if not is_supported(obj, blue+black):
					non_supported_link_objs.append(obj)
			new_coords, new_pivot, new_rotation, objectPivoted = pivot_object(o, o.pivot, non_supported_link_objs, touching_o)
			if(objectPivoted):
				objectsMoved.append(o)
				#need to move linked objects

				#need to move ropes

			# not actually right yet
			# o.coords = new_coords
			# o.pivot = new_pivot
			o.rotation = new_rotation
	# for obj in objectsMoved:
	# 	if(len(obj.attachedObjects) > 0):
	# 		#move object
	return

def run_machine(black,blue,green,imSize):
	someObjectsMoved = True
	movieImages = [make_image(black,blue,green,imSize),]
	i=0
	#while someObjectsMoved:
	while i < 20:
		i+=1
		print('Step '+str(i))
		#black[0].rotation += 1
		#check if anything changed since last frame
		someObjectsMoved = move_shapes(black,blue)
		movieImages += [make_image(black,blue,green,imSize),]
	return movieImages

def make_video(image1, images):
	height, width, layers = np.asarray(images[0]).shape

	video = cv2.VideoWriter("video.avi", -1, 15, (width,height))

	for image in images:
  		video.write(np.asarray(image))

	cv2.destroyAllWindows()
	video.release()


def main():
	image = cv2.imread("problems/pivot_test.png")
	size = np.array(image).shape
	black,blue, green, yellow = segment_objects(image)
	#print(blue)
	print(len(black),len(blue),len(green),len(yellow))
	attach_yellows(blue,yellow)
	attach_greens(blue,green)
	attach_objects(blue,black,green)
    # blueO = blue[0]
    # blackO = black[0]
    # touchingVal, orientationVal = is_touching(blueO, blackO)
    # print(orientationVal)
    #move_shapes(blue,black)
    # im = make_image(black, blue)
    # im.show()

	movie = run_machine(black,blue,green,size)
	for i,im in enumerate(movie):
		im.save('out/im-'+str(i)+'.png')
	make_video(image,movie)
    #imageToShow = segmentblu[0].image
    #Image.fromarray((1-imageToShow)*255).show()
    #print(len(segmentbl), len(segmentblu), len(segmentg), len(segmenty))
    



main()