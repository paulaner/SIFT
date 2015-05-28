import numpy
import Image


class contrast(object):

	def lowcontrast(self, arr):

	    H, W = arr.shape
	    re = []

	    for i in range(1,H-1):
                for j in range(1,W-1):
                    temp = arr[i-1:i+2,j-1:j+2]
		    winStd = temp.std()
		    winMean = temp.mean()
		    if winStd == 0:
			continue				
		    elif abs((arr[i][j] - winMean)/winStd) > 0.3:
					re.append((i,j))

            return re


# con  = contrast()
# im = Image.open('f:\\5500\\tt\\s.jpg').convert('L')
# ima = numpy.array(im)
# re = con.lowcontrast(ima)
# print len(re)
