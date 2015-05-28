from PIL import Image
import scipy
import numpy
import scipy.ndimage
import math
import itertools

import harris
import hessian
import contrast


class findextrema(object):

    def getPatextremes(self,ims,pa):
        """ 
        find local extremas on pattern image
        """

        # instantiate funtional class
        hs = harris.harris()
        hess = hessian.hessian()
        cont = contrast.contrast()

        coordinates = []
        temp = {}

        H = [0,1,2,3]
        W = [0,1,2,3]

        for i in range(4):
            H[i] = len(ims[i][0])
            W[i] = len(ims[i][0][0])

        localArea = [0,1,2]

        # get the unstable and low contrast pixel
        hs_points = hs.corner(pa)
        hess_points = hess.Patedgedetect(pa)
        low_contrast = cont.lowcontrast(pa)

        # compute the pixels which are not situable for pixel matching
        bad_points = list(set(hs_points) | set(hess_points) | set(low_contrast))
        bad = dict.fromkeys(bad_points, 0)

        for m in range(4):
            for n in range(1,3):
                for i in range(16,H[m]-16):
                    for j in range(16,W[m]-16):
                        if bad.has_key((i*2**m,j*2**m))==False :

                            # compare local pixel with its 26 neighbour
                            currentPixel = ims[m][n][i][j]                                
                            localArea[0] = ims[m][n-1][i-1:i+2,j-1:j+2]
                            localArea[1] = ims[m][n][i-1:i+2,j-1:j+2]
                            localArea[2] = ims[m][n+1][i-1:i+2,j-1:j+2]

                            Area = numpy.array(localArea) 
                                   
                            maxLocal = numpy.array(Area).max()
                            minLocal = numpy.array(Area).min()

                            if (currentPixel == maxLocal) or (currentPixel == minLocal):
                                if temp.has_key((i*2**m,j*2**m)) == False:
                                    coordinates.append([int(i*2**m),int(j*2**m)])
                                    temp[(i*2**m,j*2**m)] = [i*2**m,j*2**m]
        return coordinates


    def get_Srcextremes(self,ims,sa):
        """ 
        find local extremas on pattern image
        """

        # instantiate funtional class
        hs = harris.harris()
        hess = hessian.hessian()
        cont = contrast.contrast()

        coordinates = []
        temp = {}

        H = [0,1,2,3]
        W = [0,1,2,3]

        for i in range(4):
            H[i] = len(ims[i][0])
            W[i] = len(ims[i][0][0])

        localArea = [0,1,2]

        # get the unstable and low contrast pixel
        hs_points = hs.corner(sa)
        hess_points = hess.Srcedgedetect(sa)
        low_contrast = cont.lowcontrast(sa)

        # compute the pixels which are not situable for pixel matching
        bad_points = list(set(hs_points) | set(hess_points) | set(low_contrast))
        bad = dict.fromkeys(bad_points, 0)


        for m in range(4):
            for n in range(1,3):
                for i in range(16,H[m]-16):
                    for j in range(16,W[m]-16):
                        if bad.has_key((i*2**m,j*2**m))==False :

                            # compare local pixel with its 26 neighbour
                            currentPixel = ims[m][n][i][j]    
                            localArea[0] = ims[m][n-1][i-1:i+2,j-1:j+2]
                            localArea[1] = ims[m][n][i-1:i+2,j-1:j+2]
                            localArea[2] = ims[m][n+1][i-1:i+2,j-1:j+2]

                            Area = numpy.array(localArea) 
                                   
                            maxLocal = numpy.array(Area).max()
                            minLocal = numpy.array(Area).min()

                            if (currentPixel == maxLocal) or (currentPixel == minLocal):
                                if temp.has_key((i*2**m,j*2**m)) == False:
                                    coordinates.append([int(i*2**m),int(j*2**m)])
                                    temp[(i*2**m,j*2**m)] = [i*2**m,j*2**m]
        return coordinates

        
