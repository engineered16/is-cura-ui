# SmartSliceDrawSelection.py
# Teton Simulation
# Authored on   November 7, 2019
# Last Modified November 7, 2019

#
# Contains functionality for drawing selected meshes within Cura's Scene Node
#

#  Ultimaker/Cura Libraries
from UM.Mesh.MeshData import MeshData

#  SmartSlice UI Backend Libs
from .FaceSelection import SelectableFace

'''
  class SmartSliceSelectionVisualizer
    
    Contains functionality for drawing selected faces within Smart Slice Scene Node
'''
class SmartSliceSelectionVisualizer:
#  Constructors
    '''
      SmartSliceSelectionVisualizer([OPTIONAL] faces)
        'faces' is a list of 'SelectableFace'

        Creates a new object for visualizing selected faces on a mesh
    '''
    def __init__(self, faces = []):
        #  Set Selected Faces
        self._selected_faces = faces
        self._mesh = MeshData()


#  Accessors
    '''
      getFace(index)
        'index' is an integer value

        Returns 'SelectableFace' object at 'index' within visualizer.  
        Returns None if 'index' does not refer to a valid selected face
    '''
    def getFace(self, index):
        if index >= 0 and index < len(self._faces):
            return self._faces[index]
        else 
            return None
        

#  Mutators
  #  Single Face Mutation
    '''
      selectFace(face)
        'face' is a 'SelectableFace' object

        Adds 'face' to SmartSliceSelectionVisualizer's selected faces
    '''
    def selectFace (self, face):
        if not (face in self._faces):
            self._selected_faces.append(face)
            drawFace(face)

    '''
      deselectFace(face)
        'face' is a 'SelectableFace' object

        Removes 'face' from SmartSliceSelectionVisualizer's selected faces
    '''
    def deselectFace (self, face):
        if face in self._selected_faces:
            self._selected_faces.remove(face)
            clearFace(face)

  #  Multiple Face Mutation
    '''
      changeSelection(faces)
        'faces' is a list of 'SelectableFace' objects

        Changes actively selected faces to the newly given list of faces
    '''
    def changeSelection (self, faces):
        self._selected_faces = faces
        redrawSelection()


  #  Scene Mutation
    '''
      drawSelection()

        Draws all currently selected faces within Cura Scene
    '''
    def drawSelection(self):
        #  Clear Current Selection

        #  Draw New Selection
        for _face in self._selected_faces:
            drawFace(_face)

    '''
      clearSelection()

        Clears all selection drawings within Cura's Scene
    '''
    def clearSelection(self):
        for _face in self._selected_faces:
            clearFace(_face)

    def redrawSelection(self):
        self.clearSelection()
        self.drawSelection()

    '''
      drawFace(face)

        Draws given 'SelectableFace' object within Cura Scene
    '''
    def drawFace(self, face):
        1 + 1 #  STUB

    '''
      clearFace(face)

        Clears 'face' from selection drawings within Cura's Scene
    '''
    def clearFace(self, face):
        1 + 1 #  STUB

