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
from .FaceSelectionDecorator import FaceSelectionDecorator

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

        #  Set MeshData to Selected Face

        
        #  Add Decorator
        self._decor = FaceSelectionDecorator(self)
        self.addDecorator(self._decor)

        #  Add this SceneNode to Cura Scene
        self._scene_node.addChild(self)


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
        1 + 1  #  STUB; Not necessary yet

    '''
      clearSelection()

        Clears all selection drawings within Cura's Scene
    '''
    def clearSelection(self):
        for _face in self._selected_faces:
            self.clearFace(_face)


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


  #  Scene Mutation
    '''
      drawSelection()

        Draws all currently selected faces within Cura Scene
    '''
    def drawSelection(self):
        #  Draw New Selection
        verts = []
        norms = []

        for _face in self._selected_faces:
            #  NOTE: ASSUMES FACES ARE TESSELATED TRIANGLES
            #  TODO: Allow any face shape

            #  Add each point's coordinate components
            for _point in _face.points:
                verts.append([_point.x, _point.y, _point.z])
            #  Add each point's normal vertex
            norms.append(_face.vnormals)

        # Convert to NumPy Array for MeshData
        v = immutableNDArray(verts)
        n = immutableNDArray(norms)

        # Construct new 'MeshData' object, representative of current face selection
        md = MeshData(vertices=v, normals=n)

        # Change SceneNode's MeshData to current selection in Cura
        self._scene_node.setMeshData(md)

            
                

