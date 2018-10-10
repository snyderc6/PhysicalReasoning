import numpy as np

class SolidObject():
    
    def __init__(self,array,coords,pivot=None,isBlue=False):
        self.coords = coords
        self.image = array
        self.allpixels = np.transpose(array.nonzero())
        self.center = tuple(np.floor(np.mean(self.allpixels,axis=0)))
        self.rotation = 0
        self.area = sum(sum(array))
        self.ropeIds = []
        self.ropeAttachPoints = []
        self.pivot = pivot #make this coords of pivot
        print('Created object shape=',self.image.shape,'center=',self.center,'coords=',self.coords,'area=',self.area)