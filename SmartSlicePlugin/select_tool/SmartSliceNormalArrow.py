# SmartSliceNormalArrow.py
# Teton Simulation
# Authored on   November 11, 2019
# Last Modified November 11, 2019

#
# Contains backend functionality for displaying arrow in Cura Scene
#

import os.path

#  QML Imports 
from PyQt5.QtCore import QUrl, QObject

#  Ultimaker/Cura Imports
from UM.Application import Application
from UM.PluginRegistry import PluginRegistry

#  Selectable Faces
from .FaceSelection import SelectableFace


'''
  SmartSliceNormalArrow(sf)
    sf : SelectableFace

    Creates a QML Object containing 3D mesh of normal arrow
      * Rotation/translation properties derived from 'sf'
      * Mesh created using CylinderMesh (Arrow Shaft) and ConeMesh (Arrow Head)
'''
class SmartSliceNormalArrow(QObject):
#  CONSTRUCTORS
    def __init__(self, parent) -> None:
        super().__init__()
        
        #  Set Hooks
        self._parent = parent
        self._view = Application.getInstance().getController().getActiveView()
        

        #  Rotations (Euler Angles)
        self._rot_x = 0.
        self._rot_y = 0.
        self._rot_z = 0.

        #  Translation Coordinates
        self._coord_x = 0.
        self._coord_y = 0.
        self._coord_z = 0.

        #  Normal Vector Components (DEPREPECATED)
        self._norm_x = 0.
        self._norm_y = 0.
        self._norm_z = 0.
        
        #  If SelectableFace is provided, draw the Normal Arrow
        if parent is not None:
            #  Set Physical Properties
            self.deriveTranslation()
            self.deriveRotation()
            self.deriveNormalVector()
            
            #  Draw Arrow in Canvas
            self.drawNormalArrow()



#  ACCESSORS

    '''
      rotations()
        Returns 3-wide list of euler angles (alpha, beta, gamma)
    '''
    @property
    def rotations(self):
        return [self._rot_x, self._rot_y, self._rot_z]

    '''
      coordinates()
        Returns 3-wide list of (x, y, z) positional coordinates
    '''
    @property
    def coordinates(self):
        return [self._coord_x, self._coord_y, self._coord_z]

    '''
      normals()
        Returns 3-wide list of (x, y, z) normal unit vectors
    '''
    @property
    def normals(self):
        return [self._norm_x, self._norm_y, self._norm_z]

#  MUTATORS

    '''
      rotations(rots)
        rots : list of floats

        Accepts 3-wide list of floats ('rots') and sets corresponding rotational angles
    '''
    @rotations.setter
    def rotations(self, rots):
        self._rot_x = rots[0]
        self._rot_y = rots[1]
        self._rot_z = rots[2]

    '''
      coordinates(coords)
        coords : list of floats

        Accepts 3-wide list of floats ('coords') and sets corresponding cartesian coordinates
    '''
    @coordinates.setter
    def coordinates(self, coords):
        self._coords_x = coords[0]
        self._coords_y = coords[1]
        self._coords_z = coords[2]

    '''
      normals(norms)
        norms: list of floats

        Accepts 3-wide list of floats ('norms') and sets corresponding normal vector components
    '''
    @normals.setter
    def normals(self, norms):
        self._norm_x = norms[0]
        self._norm_y = norms[1]
        self._norm_z = norms[2]


    def addToScene(self):

        #  Get Plugin Path
        #base_path = PluginRegistry.getInstance().getPluginPath("SmartSlicePlugin")

        # Add Normal Arrow to Canvas
        #component_path = os.path.join(base_path, "SmartSliceSelectTool", "NormalArrow.qml")
        #self._view.addDisplayComponent("_NormalArrow", component_path)
        print ("\nADD NORMAL ARROW TO SCENE HERE\n")

    '''
      drawNormalArrow()
    '''
    def drawNormalArrow(self):
        1 + 1 #  STUB 

    '''
      deriveTranslation()

        Set's the normal arrow's coordinates (x, y, z) to the selected face's centroid
    '''
    def deriveTranslation(self):
        #  NOTE:  Assumes Trianglar Face
        self._coord_x = (self._parent.points[0].x + self._parent.points[1].x + self._parent.points[2].x)/3
        self._coord_y = (self._parent.points[0].y + self._parent.points[1].y + self._parent.points[2].y)/3
        self._coord_z = (self._parent.points[0].z + self._parent.points[1].z + self._parent.points[2].z)/3

    '''
      deriveRotation()

        Set's the normal arrow's euler rotation's to the selected face's rotation
    '''
    def deriveRotation(self):
        # Produce Euler Angles
        1 + 1 #  STUB 

    ''' 
      deriveNormalVector()

        Set's the normal arrow's normal vector to the selected face's normal vector
          * Necessary for Arrow Head Translation
    '''
    def deriveNormalVector(self):
        self._parent.generateNormalVector()
        self._norm_x = self._parent.normal.x()
        self._norm_y = self._parent.normal.y()
        self._norm_z = self._parent.normal.z()


