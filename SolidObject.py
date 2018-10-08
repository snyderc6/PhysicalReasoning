import numpy as np

class SolidObject():
    
    def __init__(self,array,coords):
        self.coords = coords
        self.image = array
        allpixels = np.transpose(array.nonzero())
        self.center = tuple(np.floor(np.mean(allpixels,axis=0)))
        self.ropeIds = []
        self.area = sum(sum(array))
        self.ropeAttachPoints = []
        print('Created object shape=',self.image.shape,'center=',self.center,'coords=',self.coords,'area=',self.area)