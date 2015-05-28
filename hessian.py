from PIL import Image
import numpy
import scipy
from scipy.ndimage import filters

class hessian(object):

	def __init__(self):
		self.eps = 0.000001
		self.patternEdgeThreshold = 4.1
		self.sourceEdgeThreshold = 4.1

	def patEdgeDetect(self,arr):
		"""
		takes an image array as input, return the pixels on the edges of the 
		pattern image
		"""

		imx = numpy.zeros(arr.shape)
		filters.gaussian_filter(arr, (3,3), (0,1), imx)
		imy = numpy.zeros(arr.shape)
		filters.gaussian_filter(arr, (3,3), (1,0), imy)

		Wxx = filters.gaussian_filter(imx*imx,3)
		Wxy = filters.gaussian_filter(imx*imy,3)
		Wyy = filters.gaussian_filter(imy*imy,3)

		# compute the determint and trace of the array
		Wdet = Wxx*Wyy - Wxy**2
		Wtr = Wxx + Wyy

		# This threshold value is set by (r+1)**2/r and experiments 
		Thres = self.patternEdgeThreshold
		coor = []

		Hess = Wtr**2/(Wdet+self.eps)
		re = numpy.where(Hess>Thres)
		Num = len(re[0])

		for i in range(Num):
			coor.append((re[0][i],re[1][i]))
		
		return tuple(coor)


	def Srcedgedetect(self,arr):
		"""
		takes an image array as input, return the pixels on the edges of the 
		source image
		"""

		imx = numpy.zeros(arr.shape)
		filters.gaussian_filter(arr, (3,3), (0,1), imx)
		imy = numpy.zeros(arr.shape)
		filters.gaussian_filter(arr, (3,3), (1,0), imy)

		Wxx = filters.gaussian_filter(imx*imx,3)
		Wxy = filters.gaussian_filter(imx*imy,3)
		Wyy = filters.gaussian_filter(imy*imy,3)

		# compute the determint and trace of the array
		Wdet = Wxx*Wyy - Wxy**2
		Wtr = Wxx + Wyy

		# This threshold value is set by (r+1)**2/r and experiments 
		Thres = self.sourceEdgeThreshold
		coor = []

		Hess = Wtr**2/(Wdet+self.eps)
		re = numpy.where(Hess>Thres)
		Num = len(re[0])

		for i in range(Num):
			coor.append((re[0][i],re[1][i]))
		
		return tuple(coor)
