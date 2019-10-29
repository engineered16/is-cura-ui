#   FaceDetection.py
#   Teton Simulation
#   Authored on   October 29, 2019
#   Last Modified October 29, 2019

#
#   Contains FaceDetection Class
#

import sys
sys.path.append('/usr/lib/python3.7')

#   CGAL Imports
import CGAL
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Kernel import Vector_3


'''
    FaceDetection(points)
'''
class FaceDetection:
    def __init__ ( self, points = [] ):
        self._pwn = points
        self._shapes = []

    '''
      detect()
           Uses the currently defined PointWithNormals to populate the _shapes list
           After execution, the FaceDetection object holds a list of detected selectable faces
    '''
    def detect(self):
        #  Clear cached shapes
        self._shapes = []
        for pwn in self._pwn:
            1 + 2 # STUB

    '''
      setPoints(pwns)
           Resets the list of PointWithNormals to the parameterized list
    '''
    def setPoints(self, pwns):
        self._pwn = pwns

    '''
      addPoint(pwn)
           Adds parameterized PointWithNormal pwn to the list of active points
    '''
    def addPoint(self, pwn):
        self._pwn.append(pwn)

    '''
      removePoint(pwn)
           Searchs for a PointWithNormal that matches parameter;
             * If found, removes pwn from active points
             * If not found, catch and report error
    '''
    def removePoint(self, pwn):
        self._pwn # STUB

    '''
      countShapes()
           Returns number of detected shapes.  NOTE: Does nothing without detect() first.
    '''
    def countShapes(self):
        return len(self._shapes)





class PointWithNormal:
    def __init__ (self, point, normal) :
        self._point = point
        self._normal = normal

    def getNormal(self):
        return self._normal

    def setNormal(self, normal):
        self._normal = normal

    def getPoint(self):
        return self._point

    def setPoint(self, point):
        self._point = point
