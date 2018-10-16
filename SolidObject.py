import numpy as np
from PIL import Image

class SolidObject():
    
    def __init__(self,array,coords,pivot=None,isBlue=False):
        self.coords = coords
        self.image = array
        self.base_image = array
        self.allpixels = np.transpose(array.nonzero())
        self.center = tuple(np.floor(np.mean(self.allpixels,axis=0)))
        self.rotation = 0
        self.area = sum(sum(array))
        self.ropeIds = []
        self.ropeAttachPoints = []
        self.pivot = pivot #make this coords of pivot
        self.attachedObjects = []
        print('Created object shape=',self.image.shape,'center=',self.center,'coords=',self.coords,'area=',self.area)

    def rotateImage(self,angle,updateCoords=True):
        #rotates about center of mass
        #returns new image, new list of nonzero pixels, and new coords
        #(new coords are determined by center of mass change, but could be wrong because image resizing)

        #newIm = Image.new("RGB",(500,500),"black")
        #Image.fromarray(self.image*255).show()
        newIm = Image.fromarray(self.image).rotate(angle,expand=1)
        newIm = Image.fromarray(np.round(np.array(newIm)))
        
        bbox = newIm.getbbox()
        newIm = np.array(newIm.crop(bbox))
        pixels = np.transpose(newIm.nonzero())

        newCenter = tuple(np.floor(np.mean(pixels,axis=0)))
        centerDiff = self.center[0]-newCenter[0],self.center[1]-newCenter[1]
        newCoords =  self.center[0]-centerDiff[0],self.coords[1]-centerDiff[1]
        newPivot = []
        if self.pivot:
            newPivot = self.pivot[0]-centerDiff[0],self.pivot[1]-centerDiff[1]
        if updateCoords:
            self.coords = newCoords

        return newIm, pixels, newCoords, newPivot

    def getWorldPixelCoordList(self):
        oldPivot = self.pivot
        oldCoords = self.coords
        im,vals,newCoords,newPivot = self.rotateImage(self.rotation,updateCoords=False)
        #vals = x[1]
        difference = [0,0]
        print("newCoords", self.rotation, newCoords, oldCoords)
        if oldPivot and (newPivot != oldPivot):
            print("OLD", oldPivot)
            print("NEW", newPivot)
            difference = np.asarray(oldPivot) - np.asarray(newPivot)
            print("DIFFERENCE", difference)
        for i,val in enumerate(vals):
            val[0] = val[0] + self.coords[0] + difference[0]
            val[1] = val[1] + self.coords[1] + difference[1]
            vals[i] = val
        return vals

