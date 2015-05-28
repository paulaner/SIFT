import math
import numpy

class factor(object):

    def calFactor(self,pair0,pair1,pair2):
        """
        given three pixel pairs and divide the two area of the triangle 
        whose vertices are the three pixels in those three pairs.
        """
        abPat,acPat,bcPat,ABSrc,ACSrc,BCSrc = self.dist(pair0,pair1,pair2)

        # divide the two triangles' area 
        factor = self.calArea(ABSrc,ACSrc,BCSrc)/self.calArea(abPat,acPat,bcPat)

        return factor


    def dist(self,pair0,pair1,pair2):
        """
        return the distance bewteen 3 match pixels
        """

        ax = pair0[0][0]
        ay = pair0[0][1]
        Ax = pair0[1][0]
        Ay = pair0[1][1]

        bx = pair1[0][0]
        by = pair1[0][1]
        Bx = pair1[1][0]
        By = pair1[1][1]

        cx = pair2[0][0]
        cy = pair2[0][1]
        Cx = pair2[1][0]
        Cy = pair2[1][1]
        
        dista_b = math.sqrt((ax-bx)**2+(ay-by)**2)
        dista_c = math.sqrt((ax-cx)**2+(ay-cy)**2)
        distb_c = math.sqrt((bx-cx)**2+(by-cy)**2)
        
        distA_B = math.sqrt((Ax-Bx)**2+(Ay-By)**2)
        distA_C = math.sqrt((Ax-Cx)**2+(Ay-Cy)**2)
        distB_C = math.sqrt((Bx-Cx)**2+(By-Cy)**2)
                            
        return dista_b,dista_c,distb_c,distA_B,distA_C,distB_C 


    def cal_area(self,x,y,z):
        """
        compute the area of a triangle whose side lengths are the 3 input
        """
        p = (x+y+z)/2

        # Hellen formula
        return math.sqrt(p*(p-x)*(p-y)*(p-z))

