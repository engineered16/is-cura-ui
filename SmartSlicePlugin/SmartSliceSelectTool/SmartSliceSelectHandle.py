# SmartSliceSelectHandle.py
# Teton Simulation
# Last Modified November 12, 2019

# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.

#
#   Contains functionality to be triggered upon face selection
#

from UM.Scene.ToolHandle import ToolHandle
from UM.Scene.SceneNode import SceneNode
from UM.Mesh.MeshBuilder import MeshBuilder
from UM.Mesh.MeshData import MeshData

from UM.Math.Color import Color
from UM.Math.Matrix import Matrix
from UM.Math.Quaternion import Quaternion
from UM.Math.Vector import Vector

# Local Imports
from .FaceSelection import SelectableFace
from .Detessellate import isCoplanar, isJointed

class SmartSliceSelectHandle(ToolHandle):
#  CONSTRUCTORS
    def __init__(self, parent = None, face: SelectableFace = None):
        super().__init__(parent)

        self._name = "SmartSliceSelectHandle"

        #  Default Line Properties
        self._edge_width = 0.8
        self._edge_length = [] # TODO: GET THIS FROM FACE EDGES
        self._color = self._y_axis_color

        #  Selected Face Properties
        self._face = face
        self._center = self.findCenter()

        #  Normal Vector Arrow (if applicable)
        self._arrow = None

#  ACCESSORS
    @property
    def face(self):
        return self._face

#  MUTATORS
    def setFace(self, f):
        self._face = f
        self._center = self.findCenter()


    '''
      drawFaceSelection()

        Uses UM's MeshBuilder to construct 3D Arrow mesh and translates/rotates as to be normal to the selected face
    '''
    def drawFaceSelection(self, draw_arrow = False):
        #  Construct Edges using MeshBuilder Cubes
        mb = MeshBuilder()
        sn = SceneNode(self)

        f = self._face
        
        #  Paint Face Selection
        p = f.points
        f.generateNormalVector()
        n = f.normal

        p0 = Vector(p[0].x, p[0].y, p[0].z)
        p1 = Vector(p[1].x, p[1].y, p[1].z)
        p2 = Vector(p[2].x, p[2].y, p[2].z)
        norm = Vector(n.x, n.y, n.z)
        mb.addFace(p0, p1, p2, n, self._color)

        if draw_arrow:
            #  Paint Normal Arrow   
            center_shaft = Vector(self._center[0], self._center[1]+5, self._center[2])
            center_head = Vector(self._center[0], self._center[1]+10, self._center[2])

            mb.addCube(1, 10, 1, center_shaft, self._color)
            mb.addPyramid(5, 5, 5, 0, Vector.Unit_Y, center_head, self._color)
            
            mat = Matrix()
            mat.setByRotationAxis(180*n.x, Vector.Unit_X)
            mat.setByRotationAxis(-180*(1-n.y), Vector.Unit_Y)
            mat.setByRotationAxis(180*n.z, Vector.Unit_Z)

            sn.rotate(Quaternion().fromMatrix(mat))

        #  Add to Cura Scene
        self.setSolidMesh(mb.build())


    '''
      findCenter()

        calculates center vector for currently selected face
    '''
    def findCenter(self):
        i = 0
        x = 0.
        y = 0.
        z = 0.

        if self._face is None:
            return [0, 0, 0]

        for p in self._face.points:
            
            x += p.x
            y += p.y
            z += p.z
            
            i += 1

        return [x/i, y/i, z/i]
