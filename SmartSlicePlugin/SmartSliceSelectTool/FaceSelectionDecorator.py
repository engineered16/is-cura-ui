# FaceSelectionDecorator.py
# Teton Simulation
# Authored on   November 8, 2019
# Last Modified November 9, 2019

#
# Contains object for colorizing face selection MeshData
#


#  UM Imports
from UM.Mesh import MeshData
from UM.Scene.SceneNode import SceneNode
from UM.Scene.SceneNodeDecorator import SceneNodeDecorator


'''
  FaceSelectionDecorator(node)
    node: SceneNode

    Creates a SceneNodeDecorator for colorizing a FaceSelection SceneNode
'''
class FaceSelectionDecorator(SceneNodeDecorator):

#  CONSTRUCTORS
    def __init__(self, parent: "SceneNode") -> None:
        super().__init__()
        self._parent = parent

        #  Get Mesh Data
        self._mesh = parent.getMeshData()



#  ACCESSORS
    @property
    def parent(self) -> SceneNode:
        return self._parent



#  MUTATORS
    @parent.setter
    def parent(self, node: "SceneNode"):
        self._parent = node

