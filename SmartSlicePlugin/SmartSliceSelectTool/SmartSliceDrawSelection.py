# SmartSliceDrawSelection.py
# Teton Simulation
# Authored on   November 7, 2019
# Last Modified November 8, 2019

#
# Contains functionality for drawing selected meshes within Cura's Scene Node
#

#  Ultimaker/Cura Libraries
from UM.Application import Application
from UM.Scene import Scene
from UM.Scene.SceneNode import SceneNode
from UM.Mesh.MeshData import MeshData

#  Geometry Manipulation Libs
from UM.Math.NumPyUtil import immutableNDArray
from CGAL.CGAL_Kernel import Point_3, Vector_3

#  SmartSlice UI Backend Libs
from .FaceSelection import SelectableFace

'''
  class SmartSliceSelectionVisualizer
    
    Contains functionality for drawing selected faces within Smart Slice Scene Node
'''
class SmartSliceSelectionVisualizer(SceneNode):
#  Constructors
    '''
      SmartSliceSelectionVisualizer([OPTIONAL] faces)
        'faces' is a list of 'SelectableFace'

        Creates a new object for visualizing selected faces on a mesh
    '''
    def __init__(self, faces = []):
        super().__init__()
        #  Set Selected Faces
        self._selected_faces = faces

        #  Get Copy of Scene
        self._scene_node = Application.getInstance().getController().getScene().getRoot()

        #  Define Selection Color Codes
        self.ActiveBlue = [100, 100, 255]
        self.InactiveBlack = [0, 0, 0]

        #  Add this SceneNode to Cura Scene
        self._scene_node.addChild(self)
        
        #  Add Decorator && Paint Selected Faces
        self.drawSelection()


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
        else:
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
            #  Set Attributes
            face.select()

            #  Add to Selection Object and Draw in Canvas
            self._selected_faces.append(face)

    '''
      deselectFace(face)
        'face' is a 'SelectableFace' object

        Removes 'face' from SmartSliceSelectionVisualizer's selected faces
    '''
    def deselectFace (self, face):
        if face in self._selected_faces:
            self._selected_faces.remove(face)

    def clearFace (self, face):
        self.deselectFace(face)
        # TODO: Remove Face from MeshData

    '''
      clearSelection()
        Clears all selection drawings within Cura's Scene
    '''
    def clearSelection(self):
        for _face in self._selected_faces:
            self.clearFace(_face)

  #  Scene Mutation
    '''
      drawSelection()
        Draws all currently selected faces within Cura Scene
    '''
    def drawSelection(self):

        #  Create MeshData using Selected Faces
        v = []
        n = []
        i = []
        c = []

        #  Add each selected face to MeshData
        for _face in self._selected_faces:
            j = []
            index = 0
            for _point in _face.points:
                v.append([_point.x, _point.y, _point.z])
                j.append(index)
                index += 1
            n.append(_face.vnormals)
            i.append(j)
            c.append(self.ActiveBlue)

        #  Define/Set the MeshData
        md = MeshData(v, n, i, c)
        self.setMeshData(md)

    '''
      redrawSelection()
        Clears current selection scene and draws new scene with current MeshData
    '''
    def redrawSelection(self):
        self.clearSelection()
        self.drawSelection()


  #  Multiple Face Mutation
    '''
      changeSelection(faces)
        'faces' is a list of 'SelectableFace' objects

        Changes actively selected faces to the newly given list of faces
    '''
    def changeSelection (self, faces):
        self._selected_faces = faces
        self.redrawSelection()

            
                

