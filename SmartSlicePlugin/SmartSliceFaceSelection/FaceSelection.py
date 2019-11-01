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
from Facet import SelectableFace
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

