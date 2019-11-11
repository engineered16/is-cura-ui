# SmartSliceNormalArrow.py
# Teton Simulation
# Authored on   November 11, 2019
# Last Modified November 11, 2019

#
# Contains backend functionality for displaying arrow in Cura Scene
#


#  QML Imports 
from PyQt5.QtCore import QUrl, QObject


'''
  SmartSliceNormalArrow(sf)
    sf : SelectableFace

    Creates a QML Object containing 3D mesh of normal arrow
      * Rotation/translation properties derived from 'sf'
      * Mesh created using CylinderMesh (Arrow Shaft) and ConeMesh (Arrow Head)
'''
class SmartSliceNormalArrow(QObject):
#  CONSTRUCTORS
    def __init__(self, parent : SelectableFace) -> None:
        super().__init__()
        
        self._parent = parent


#  ACCESSORS


#  MUTATORS
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
        1 + 1 #  STUB

    '''
      deriveRotation()

        Set's the normal arrow's euler rotation's to the selected face's rotation
    '''
    def deriveRotation(self):
        1 + 1 #  STUB 

    ''' 
      deriveNormalVector()

        Set's the normal arrow's normal vector to the selected face's normal vector
          * Necessary for Arrow Head Translation
    '''
    def deriveNormalVector(self):
        1 + 1 #  STUB


