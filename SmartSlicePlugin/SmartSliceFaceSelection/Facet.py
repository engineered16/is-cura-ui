# Facet.py
# Teton Simulation
# Authored on   November 1, 2019
# Last Modified November 1, 2019

#
# Contains definitions for Cura Smart Slice Facets (Face)
#

#  STANDARD IMPORTS (FOR TESTING)
import sys, os
sys.path.append('/usr/lib/python3')
sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append(os.getcwd())

import CGAL
from CGAL.CGAL_Kernel import Point_3, Vector_3


''' 
  SelectableFace(points, normal)
    Contains definition for a shape face with a normal vector
'''
class SelectableFace:
    def __init__(self, points, normal):
        self._points = points
        self._edges = []
        self.generateEdges()
        self._normal = normal
        self._selected = False


  #  ACCESSORS

    '''
      points()
        Returns the list of Point_3 that defines the FaceWithNormal
    '''
    @property
    def points(self):
        return self._points

    @property
    def edges(self):
        return self._edges

    '''
      normal()
        Returns the FaceWithNormal's Normal Vector_3
    '''
    @property
    def normal(self):
        return self._normal

    '''  selected()
        Returns true if face is selected
                false otherwise
    '''
    @property
    def selected(self):
        return self._selected

    '''
      getPoint(i)
        Returns the PointWithNormal at index: i
    '''
    def getPoint(self, i):
        return self._points[i]

    ''' 
      printDetails()
        Gives a printout of meaningful properties regarding SelectableFace
    '''
    def printDetails(self):
        print ("# of Points:  " + str(len(self._points)))
        for p in self._points:
            print ("Point: (" + str(p.x()) + ", " + str(p.y()) + ", " + str(p.z()) + ")")
        print ("\n")


  #  MUTATORS

    '''
      addPoint()
        If there is no conflict, adds PointWithNormal to FaceWithNormal
    '''
    def addPoint(self, point):
        self._points.append(point)

    ''' 
      selected(isSelected)
        Changes SelectableFace status to 'isSelected'
    '''
    @selected.setter
    def selected(self, isSelected):
        self._selected = isSelected

    def select(self):
        self._selected = True

    def deselect(self):
        self._selected = False

    '''
      addTri()
        Adds triangle to SelectableFace
    '''
    def addTri(self, tri):
        #  Add Points to Face if Necessary
        for p in tri.points:
            _add = True
            for q in self._points:
                #  If Vertex is already in face...
                if ((p.x() == q.x()) and (p.y() == q.y()) and (p.z() == q.z())):
                    _add = False
            if (_add):
                #  Add Point and Associated Edges to Face
                self.addPoint(p)
                for p2 in tri.points:
                    if (p != p2):
                        self.addEdge(p, p2)
        
  

    '''
      generatedEdges()
        Sets Facet edges to be the outline of the shape
    '''
    def generateEdges(self):
        #  ASSUMES STARTING FACET IS TRIANGLE FOR NOW
        self._edges = [Edge(self._points[0], self._points[1])]
        self._edges.append(Edge(self._points[0], self._points[2]))
        self._edges.append(Edge(self._points[1], self._points[2]))

    def addEdge(self, p1, p2):
        self._edges.append(Edge(p1, p2))

    '''
      removeEdge(edge)
        If 'edge' is in the SelectableFace, remove it
    '''
    def removeEdge(self, edge):
        for e in self._edges:
            if ((edge.p1 == e.p1 and edge.p2 == e.p2) or (edge.p1 == e.p2 and edge.p2 == e.p1)):
                self._edges.remove(e)

    '''
      generateNormalVector()
        Returns the cross product of the first three points within the Face

        This makes the assumption that all other points beyond p3 are COPLANAR
    '''
    def generateNormalVector(self):
        vec1 = Vector_3(self._points[1].x() - self._points[0].x(), self._points[1].y() - self._points[0].y(), self._points[1].z() - self._points[0].z())
        vec2 = Vector_3(self._points[2].x() - self._points[0].x(), self._points[2].y() - self._points[0].y(), self._points[2].z() - self._points[0].z())
        cross_x = vec1.y()*vec2.z() - vec1.z()*vec2.y()
        cross_y = vec1.z()*vec2.x() - vec1.x()*vec2.z()
        cross_z = vec1.x()*vec2.y() - vec1.y()*vec2.x()
        cross   = (cross_x*cross_x) + (cross_y*cross_y) + (cross_z*cross_z)
        self._normal = Vector_3(cross_x/cross, cross_y/cross, cross_z/cross)




class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2



'''
    NormalVector(p1, p2, p3)
    Returns the cross product of the first three points within the Face

    This makes the assumption that all other points beyond p3 are COPLANAR
'''
def NormalVector(p0, p1, p2):
    vec1 = Vector_3(p1.x() - p0.x(), p1.y() - p0.y(), p1.z() - p0.z())
    vec2 = Vector_3(p2.x() - p0.x(), p2.y() - p0.y(), p2.z() - p0.z())
    cross_x = vec1.y()*vec2.z() - vec1.z()*vec2.y()
    cross_y = vec1.z()*vec2.x() - vec1.x()*vec2.z()
    cross_z = vec1.x()*vec2.y() - vec1.y()*vec2.x()
    cross   = (cross_x*cross_x) + (cross_y*cross_y) + (cross_z*cross_z)
    return Vector_3(cross_x/cross, cross_y/cross, cross_z/cross)
