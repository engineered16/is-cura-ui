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
from CGAL.CGAL_Kernel import COPLANAR

'''
    FaceDetection(points)
'''
class FaceDetection:
    def __init__ ( self, points = [] ):
        self._pwns = points
        #  STAGE ONE:  Get Normal x, y, Z
        #    *  If a normal vector component is already in _possible_*, add to _possible_normals
        #    *  Otherwise, add component to possible cartesian list
        self._discovered_x = []
        self._discovered_y = []
        self._discovered_z = []
        #  STAGE TWO:  A second point shares a normal vector component with a first point
        #
        self._possible_vertices  = []
        #  STAGE THREE: 
        #
        self._extracted_shapes = []

    '''
      detect()
           Uses the currently defined PointWithNormals to populate the _shapes list
           After execution, the FaceDetection object holds a list of detected selectable faces
    '''
    def detect(self):
        self.clear()
        for pwn in self._pwns:
            #  Analyze x
            if (self._discovered_x.count(pwn.getNormal().x()) < 2):
                self._discovered_x.append(pwn.getNormal().x())
                self._possible_vertices.append(pwn)
            elif (self._discovered_x.count(pwn.getNormal().x()) == 2):
                self._discovered_x.append(pwn.getNormal().x())
                vertices = [ pwn.getPoint() ]
                for vert in self._possible_vertices:
                    if (vert.getNormal().x() == pwn.getNormal().x()):
                        vertices.append( vert.getPoint() )
                self._extracted_shapes.append(FaceWithNormal(vertices))
            #  Analyze y
            if (self._discovered_y.count(pwn.getNormal().y()) < 2):
                self._discovered_y.append(pwn.getNormal().y())
                self._possible_vertices.append(pwn)
            elif (self._discovered_y.count(pwn.getNormal().y()) == 2):
                self._discovered_y.append(pwn.getNormal().y())
                vertices = [ pwn.getPoint() ]
                for vert in self._possible_vertices:
                    if (vert.getNormal().y() == pwn.getNormal().y()):
                        vertices.append( vert.getPoint() )
                self._extracted_shapes.append(FaceWithNormal(vertices))
            #  Analyze Z
            if (self._discovered_z.count(pwn.getNormal().z()) < 2):
                self._discovered_z.append(pwn.getNormal().z())
                self._possible_vertices.append(pwn)
            elif (self._discovered_z.count(pwn.getNormal().z()) == 2):
                self._discovered_z.append(pwn.getNormal().z())
                vertices = [ pwn.getPoint() ]
                for vert in self._possible_vertices:
                    if (vert.getNormal().z() == pwn.getNormal().z()):
                        vertices.append( vert.getPoint() )
                self._extracted_shapes.append(FaceWithNormal(vertices))

    '''
      setPoints(pwns)
           Resets the list of PointWithNormals to the parameterized list
    '''
    def setPoints(self, pwns):
        self._pwns = pwns

    '''
      addPoint(pwn)
           Adds parameterized PointWithNormal pwn to the list of active points
    '''
    def addPoint(self, pwn):
        self._pwns.append(pwn)

    '''
      removePoint(pwn)
        Searchs for a PointWithNormal that matches parameter;
          * If found, removes pwn from active points
          * If not found, catch and report error
    '''
    def removePoint(self, pwn):
        self._pwns # STUB

    '''
      countShapes()
        Returns number of detected shapes.  NOTE: Does nothing without detect() first.
    '''
    def count(self):
        return len(self._extracted_shapes)

    '''
      clear()
        Clears extracted/possible shape lists
    '''
    def clear(self):
        self._extracted_shapes = []
        self._possible_normals = []


'''
    PointWithNormal(point, normal)
'''
class PointWithNormal:
    def __init__ (self, point, normal) :
        self._point = point
        self._normal = normal

    '''
      getNormal()
        Returns a PointWithNormal's Normal Vector_3
    '''
    def getNormal(self):
        return self._normal

    '''
      setNormal(normal)
        Sets a PointWithNormal's Normal Vector to parameterized Vector_3
    '''
    def setNormal(self, normal):
        self._normal = normal

    '''
      getPoint()
        Returns a handle to PointWithNormal's Point_3 
    '''
    def getPoint(self):
        return self._point

    '''
      setPoint(point)
        Sets a PointWithNormal's Coordinates to parameterized Point_3
    '''
    def setPoint(self, point):
        self._point = point


'''
    FaceWithNormal(points, normal)
'''
class FaceWithNormal:
    def __init__(self, points):
        self._points = points

    '''
      getPoints()
        Returns the list of Point_3 that defines the FaceWithNormal
    '''
    def getPoints(self):
        return self._points

    '''
      getNormal()
        Returns the FaceWithNormal's Normal Vector_3
    '''
    def getNormal(self, points):
        vec1 = Vector_3(points[1].getPoint().x() - points[0].getPoint().x(), points[1].getPoint().y() - points[0].getPoint().y(), points[1].getPoint().Z() - points[0].getPoint().Z())
        vec2 = Vector_3(points[2].getPoint().x() - points[0].getPoint().x(), points[2].getPoint().y() - points[0].getPoint().y(), points[2].getPoint().Z() - points[0].getPoint().Z())
        return getCrossProduct(vec1, vec2)



#
#   HELPER FUNCTIONS
#
def getCrossProduct(self, vec1, vec2):
    cross_x = vec1.y()*vec2.z() - vec1.z()*vec2.y()
    cross_y = vec1.z()*vec2.x() - vec1.x()*vec2.z()
    cross_z = vec1.x()*vec2.y() - vec1.y()*vec2.x()
    cross   = (cross_x*cross_x) + (cross_y*cross_y) + (cross_z*cross_z)
    return Vector_3(cross_x/cross, cross_y/cross, cross_z/cross)

