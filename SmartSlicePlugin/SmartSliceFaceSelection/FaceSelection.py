# FaceSelection.py
# Teton Simulation
# Authored on   October 31, 2019
# Last Modified October 31, 2019

#
# Contains code for Face Selection
#


#  STANDARD IMPORTS
import sys, os
sys.path.append('/usr/lib/python3')
sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append(os.getcwd())

#  CGAL IMPORTS
import CGAL
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Kernel import Vector_3

#  NUMPY IMPORTS
import numpy
from stl import mesh

#  Local Imports
from Detessellate import detessellate


''' 
  FaceSelection()
    Contains functionality for determining selected face in file
'''
class FaceSelection():

  #  CONSTRUCTORS

    ''' 
      FaceSelection( OPTIONAL faces )
        Default Constructor:  Returns a new FaceSelection object.
                              If 'faces' is provided, sets _faces
    '''
    def __init__(self, tris = []):
        self._tris = tris
        self._faces = detessellate(tris)
        self._selected = [] 

    '''
      from_stl(filename)
        Returns constructor to new FaceSelection object using data from *.stl file: 'filename'
    '''
    def from_stl(self, filename):
        _mesh = mesh.Mesh.from_file(filename)
        _faces = []

        return FaceSelection(_faces)

  #  ACCESSORS

    ''' 
      faces()
        Returns list of SelectableFace in current FaceSelection object
    '''
    @property
    def faces(self):
        return self._faces

    '''
      getFace(face)
    '''
    def getFace(self, face):
        return self._faces[face]

    ''' 
      selected_faces()
        Returns list of SelectableFace that are currently selected
    '''
    @property
    def selected_faces(self):
        return self._selected

  #  MUTATORS

    ''' faces(faces)
      Changes set of detected faces to given 'faces' list
    '''
    @faces.setter
    def faces(self, faces):
        self._faces = faces
    
    ''' 
      selected_faces(faces)
        Changes active selection to list: 'faces'
    '''
    @selected_faces.setter
    def selected_faces(self, faces):
        #  TODO:  TRIGGER FACE SELECTION CHANGES HERE
        self._selected = faces

    ''' 
      select_face(face)
        Adds given 'face' to active selection
    '''
    def select_face(self, face):
        self._selected.append(face)

    ''' 
      clear_selection()
        Removes all faces from active selection
    '''
    def clear_selection(self):
        self._selected = []

    def detessellate(self):
        detessellate(self._tris)

''' 
  SelectableFace(points, normal)
    Contains definition for a shape face with a normal vector
'''
class SelectableFace:
    def __init__(self, points, normal):
        self._points = points
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


#
#   HELPER FUNCTIONS
#
def NormalVector(p1, p2, p3):
    vec1 = Vector_3(p2.x() - p1.x(), p2.y() - p1.y(), p2.z() - p1.z())
    vec2 = Vector_3(p3.x() - p1.x(), p3.y() - p1.y(), p3.z() - p1.z())
    cross_x = vec1.y()*vec2.z() - vec1.z()*vec2.y()
    cross_y = vec1.z()*vec2.x() - vec1.x()*vec2.z()
    cross_z = vec1.x()*vec2.y() - vec1.y()*vec2.x()
    cross   = (cross_x*cross_x) + (cross_y*cross_y) + (cross_z*cross_z)
    return Vector_3(cross_x/cross, cross_y/cross, cross_z/cross)
