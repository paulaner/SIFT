from PIL import Image
import scipy
import numpy
import scipy.ndimage


class process(object):
    def __init__(self):
        self.sigma = 1.6

    def createdog(self,imagearr):
        """
        return a list of image arrays containning four octaves, 
        each ovtives has four dog image arrays
        """
        re = [0,1,2,3]
        re[0] = self.diff(self.gs_blur(self.sigma,imagearr))
        for i in range(1,4):
            base = self.sampling(re[i-1][2])
            re[i] = self.diff(self.gs_blur(self.sigma, base))
        return re


    def diff(self,images):
        """ 
        generate 4 difference gaussian images
        input: a list of images in array form, the number of the list is five
        return: a list contains four images in image form, which are generated 
        by the gaussian difference operation.
        """
        diffArray = [0,1,2,3]

        # compute the difference bewteen two adjacent images in the same ovtave
        for i in range(1,5):
            diffArray[i-1] = images[i]-images[i-1]

        return numpy.array(diffArray)


    def gs_blur(self,k,img):
        """ 
        use gaussina blur to generate five images in different sigma value
        input: a k as constant, and an image in array form
        return: a list contains five images in image form which are blurred
        """
        SIG = self.sigma
        sig = [SIG,k*SIG,k*k*SIG,k*k*k*SIG,k*k*k*k*SIG]
        gsArray = [0,1,2,3,4]
        scaleImages = [0,1,2,3,4]
        
        for i in range(5):
            gsArray[i] = scipy.ndimage.filters.gaussian_filter(img,sig[i])

        return gsArray


    def normalize(self,arr):
        """
        normalize the pixel intensity
        """
        arr = arr/(arr.max()/255.0)
        return arr


    def sampling(self,arr):
        """ 
        do the equal-distance sampling to resize the oringal
        image to its 1/4
        input: an image in image form
        return: a shrinked image in image form
        """
        H=0
        W=0
        if arr.shape[0]%2 == 0:
            H = arr.shape[0]/2
        else:
            H = 1+arr.shape[0]/2

        if arr.shape[1]%2 == 0:
            W = arr.shape[1]/2
        else:
            W = 1+arr.shape[1]/2
        
        new_arr = numpy.zeros((H,W),dtype = numpy.int)
        for i in range(H):
            for j in range(W):
                new_arr[i][j] = arr[2*i][2*j]
        return new_arr
