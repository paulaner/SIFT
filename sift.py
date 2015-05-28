"""
author: alan

zhougf01@gmail.com

"""
import Image
import numpy
import scipy
import scipy.ndimage
import scipy.spatial
from scipy.ndimage import filters
from scipy.spatial import cKDTree
import math
import itertools

import process
import findextrema
import descriptor
import harris
import hessian
import factor

class sift(object):
    def __init__(self):
        self.distanceThresh = 0.00000000001
        self.similarityThresh = 0.8

    def match(self,patname,srcname):
        """
        given a pattern image and a source image, return the match result and
        the scaling factor  
        """
        
        p = Image.open(patname).convert('L')
        pa = numpy.array(p)
        pa *= 255.0/pa.max()

        s = Image.open(srcname).convert('L')
        sa = numpy.array(s)
        sa *= 255.0/sa.max()

        pre = process.process()
        ex= findextrema.findextrema()
        des = descriptor.descriptor()
        scale = factor.factor()
        
        
        pdata = pre.creatdog(pa)
        sdata = pre.creatdog(sa)
        
        pDes = []
        sDes = []

        # dict to store all the feature matching result
        result = {}

        pFeatures = ex.get_Patextremes(pdata,pa)
        sFeatures = ex.get_Srcextremes(sdata,sa)

        # assign decriptors for each feature points
        pDes = des.creatDes(pFeatures,pa)
        sDes = des.creatDes(sFeatures,sa)

        tree = []

        if sDes=={} or pDes=={}:
            return False
        else:
            # use cKD tree struture to compute the two similar pixels
            tree = scipy.spatial.cKDTree(sDes.values())
            slocList = sDes.keys()
            pDict = {}
            sDict = {}
            for p in pDes.keys():
                x = pDes[p]
                re = tree.query(x,k=2,eps=self.distanceThresh,p=2,
                    distance_upper_bound=numpy.inf)

                if re[0][1]!=0 and re[0][0]/re[0][1] < self.similarityThresh:
                    pLoc = p
                    sLoc = slocList[re[1][0]]
                    distance = re[0][0]
                    
                    # did not been compared before
                    if sDict.has_key(sLoc)==False:
                        
                        # add the result and compared pattern pixel
                        # and source pixel 
                        result[(pLoc,sLoc)] = distance
                        pDict[pLoc] = sLoc
                        sDict[sLoc] = pLoc
                    
                    elif distance < result.get((sDict[sLoc],sLoc)):

                        # updates the result and compared pattern pixel
                        # and source pixel
                        del result[(sDict[sLoc],sLoc)]
                        result[(pLoc,sLoc)] = distance
                        del pDict[sDict[sLoc]]
                        pDict[pLoc] = sLoc
                        sDict[sLoc] = pLoc
                
                elif re[0][1]==0:
                    pLoc = p
                    sLoc = slocList[re[1][0]]
                    distance = re[0][0]
                    
                    # did not been compared before
                    if sDict.has_key(sLoc)==False:

                        # add the result and compared pattern pixel
                        # and source pixel
                        result[(pLoc,sLoc)] = distance
                        pDict[pLoc] = sLoc
                        sDict[sLoc] = pLoc
                    
                    elif distance < result.get((sDict[sLoc],sLoc)):

                        # updates the result and compared pattern pixel
                        # and source pixel
                        del result[(sDict[sLoc],sLoc)]
                        result[(pLoc,sLoc)] = distance
                        del pDict[sDict[sLoc]]
                        pDict[pLoc] = sLoc
                        sDict[sLoc] = pLoc

        # the list of matched pixels, sorted by the distance
        finResult = sorted(result.items(), reverse=False, key=lambda d: d[1])
        
        match1 = finResult[0][0]
        match2 = finResult[1][0]
        match3 = finResult[2][0]

        scalingFactor = scale.cal_factor(match1,match2,match3)

        return finResult,scalingFactor
