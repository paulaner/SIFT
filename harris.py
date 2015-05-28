#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import numpy
import scipy
from scipy.ndimage import filters

# threshold = 0.0001
# eps = 0.000001

class harris(object):
    def __init__(self):
        self.threshold = 0.0001
        self.eps = 0.000001

    def corner(self,arr):
        """
        takes an image array as input and return the pixels 
        which are corners of the image
        """
        harrisim = self.compute_harris_response(arr)
        filtered_coords = self.get_harris_points(harrisim, 3, self.threshold)
        return filtered_coords

    def compute_harris_response(self,im,sigma=1.5):
        """ Compute the Harris corner detector response function
        for each pixel in a graylevel image. """

        # derivatives
        imx = numpy.zeros(im.shape)
        filters.gaussian_filter(im, (sigma,sigma), (0,1), imx)
        imy = numpy.zeros(im.shape)
        filters.gaussian_filter(im, (sigma,sigma), (1,0), imy)

        # compute components of the Harris matrix
        Wxx = filters.gaussian_filter(imx*imx,sigma)
        Wxy = filters.gaussian_filter(imx*imy,sigma)
        Wyy = filters.gaussian_filter(imy*imy,sigma)
        
        # determinant and trace
        Wdet = Wxx*Wyy - Wxy**2
        Wtr = Wxx + Wyy+self.eps

        return Wdet / Wtr

    def get_harris_points(self,harrisim,min_dist,threshold):
        """ 
        Return corners from a Harris response image
        min_dist is the minimum number of pixels separating
        corners and image boundary. 
        """

        # find top corner candidates above a threshold
        corner_threshold = harrisim.max() * self.threshold
        
        harrisim_t = (harrisim > corner_threshold) * 1

        # get coordinates of candidates
        coords = numpy.array(harrisim_t.nonzero()).T

        # ...and their values
        candidate_values = [harrisim[c[0],c[1]] for c in coords]

        # sort candidates
        index = numpy.argsort(candidate_values)

        # store allowed point locations in array
        allowed_locations = numpy.zeros(harrisim.shape)
        
        allowed_locations[min_dist:-min_dist,min_dist:-min_dist] = 1

        # select the best points taking min_distance into account
        filtered_coords = []
        for i in index:
            if allowed_locations[coords[i,0],coords[i,1]] == 1:
                filtered_coords.append(tuple(coords[i]))
                
                allowed_locations[(coords[i,0]-min_dist):(coords[i,0]+min_dist),
                        (coords[i,1]-min_dist):(coords[i,1]+min_dist)] = 0
        
        return tuple(filtered_coords)
