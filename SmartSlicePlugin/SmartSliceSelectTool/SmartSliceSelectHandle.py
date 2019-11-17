# SmartSliceSelectHandle.py
# Teton Simulation
# Last Modified November 12, 2019

# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.

#
#   Contains functionality to be triggered upon face selection
#


#  UM/Cura Imports
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
from .FaceSelection import toCalculatableFace
from .Detessellate import isCoplanar, isJointed
from .SmartSliceSelectionProxy import SmartSliceSelectionConnector


# Provides enums
class SelectionMode:
    AnchorMode = 1
    LoadMode = 2

class SmartSliceSelectHandle(ToolHandle):
#  CONSTRUCTORS
    def __init__(self, parent = None, tri: SelectableFace = None):
        super().__init__(parent)

        self._name = "SmartSliceSelectHandle"
        self._connector = SmartSliceSelectionConnector()

        #  Default Line Properties
        self._edge_width = 0.8
        self._edge_length = [] # TODO: GET THIS FROM FACE EDGES
        self._selected_color = self.AllAxisSelectionColor
        self._anchored_color = self._y_axis_color
        self._loaded_color = self._y_axis_color

        #  Selected Face Properties
        self._tri = tri
        self._face = []
        self._center = self.findCenter()

        #  Previously Selected Faces
        self._loaded_faces = []
        self._load_magnitude = 0
        self._anchored_faces = []

        #   Arrow Mesh
        self._arrow = None
        
        #  Disable auto scale
        self._auto_scale = False



#  ACCESSORS
    @property
    def face(self):
        return self._tri

#  MUTATORS
    def setFace(self, f):
        self._tri = f
        self._center = self.findCenter()

    def getLoadVector(self):
        load_mag = self._connector._proxy._loadMagnitude
        if len(self._loaded_faces) > 0:
            lf = toCalculatableFace(self._loaded_faces[0])
            n = lf.normal
            return Vector(load_mag*n.x, load_mag*n.y, load_mag*n.z)
        return None


    '''
      drawFaceSelection()

        Uses UM's MeshBuilder to construct 3D Arrow mesh and translates/rotates as to be normal to the selected face
    '''
    def drawFaceSelection(self, mode, draw_arrow = False, other_faces = []):
        #  Construct Edges using MeshBuilder Cubes
        mb = MeshBuilder()

        f = self._tri
        self._face = []
        checked = []
        if mode == SelectionMode.LoadMode:
            self._loaded_faces = []
            self._load_magnitude = 10
        if mode == SelectionMode.AnchorMode:
            self._anchored_faces = []

        #if draw_arrow:
        #    self.drawNormalArrow()
        #    self.addChild(self._arrow)

        for _tri in other_faces:
            added = False
            if isCoplanar(f, _tri) and isJointed(f, _tri):
                #  Paint Face Selection
                self.paintFace(_tri, mb)
                self._face.append(_tri)
                added = True
                if mode == SelectionMode.LoadMode:
                    self._loaded_faces.append(_tri)
                else:
                    self._anchored_faces.append(_tri)
                
                #  Paint Faces that are recursively coplanar/jointed
                self.paintPossibleFaces(mode, mb, _tri, checked)

            #  Check if Jointed/Coplanar with already selected face
            for t in self._face:
                if (t == _tri):
                    1 + 1
                elif isCoplanar(t, _tri) and isJointed(t, _tri):
                    #  Paint Face Selection
                    self.paintFace(_tri, mb)
                    self._face.append(_tri)
                    added = True
                    if mode == SelectionMode.LoadMode:
                        self._loaded_faces.append(_tri)
                    else:
                        self._anchored_faces.append(_tri)
                
                    #  Paint Faces that are recursively coplanar/jointed
                    self.paintPossibleFaces(mode, mb, _tri, checked)

            if isCoplanar(f, _tri):
                checked.append(_tri)

        #  Add to Cura Scene
        self.setSolidMesh(mb.build())  
        
        lv = self.getLoadVector()
        if self.getLoadVector() is not None:
            print ("NORMAL FORCE: (" + str(lv.x) + ", " + str(lv.y) + ", " + str(lv.z) + ")")


    '''
      paintFace(tri, mb)
        tri: SelectableFace (EXACTLY 3 Vertices)
        mb: MeshBuilder

        Creates a face representitive of 'tri' within mb and paints it selected color
    '''
    def paintFace(self, tri, mb):
        p = tri.points
        tri.generateNormalVector()
        n = tri.normal
        p0 = Vector(p[0].x, p[0].y, p[0].z)
        p1 = Vector(p[1].x, p[1].y, p[1].z)
        p2 = Vector(p[2].x, p[2].y, p[2].z)
        norm = Vector(n.x, n.y, n.z)
        mb.addFace(p0, p1, p2, n, self._selected_color)

    '''
      paintPossibleFaces(mb, face, possible)
        mb: MeshBuilder
        face: SelectableFace
        possible: List of SelectableFaces

        Paints all SelectableFaces in 'possible' that are jointed/coplanar with 'face'
        NOTE:  This assumes all entries in 'possible' are coplanar with 'face'
    '''
    def paintPossibleFaces(self, mode, mb, face, possible):
        for _tri in possible:
            if isJointed(face, _tri):
                self.paintFace(_tri, mb)
                self._face.append(_tri)
                possible.remove(_tri)
                self.paintPossibleFaces(mode, mb, _tri, possible)
                if mode == SelectionMode.LoadMode:
                    self._loaded_faces.append(_tri)
                else:
                    self._anchored_faces.append(_tri)

    '''
      paintAnchoredFaces()

        Repaints the saved selection for applied Anchors
    '''
    def paintAnchoredFaces(self):
        mb = MeshBuilder()
        for _tri in self._anchored_faces:
            self.paintFace(_tri, mb)
        #  Add to Cura Scene
        self.setSolidMesh(mb.build())  

    '''
      paintLoadedFaces()

        Repaints the saved selection for applied Loads
    '''
    def paintLoadedFaces(self):
        mb = MeshBuilder()
        for _tri in self._loaded_faces:
            self.paintFace(_tri, mb)
        #  Add to Cura Scene
        self.setSolidMesh(mb.build())  


    '''
      drawNormalArrow()
    '''
    def drawNormalArrow(self):
        mb = MeshBuilder()
        if self._arrow is not None:
            self.removeChild(self._arrow)
        self._arrow = SceneNode(self, name="_NormalArrow")

        f = self._tri
        n = f.generateNormalVector()

        #  Paint Normal Arrow
        center_shaft = Vector(self._center[0], self._center[1]+5, self._center[2])
        center_head = Vector(self._center[0], self._center[1]+10, self._center[2])

        mb.addCube(1, 10, 1, center_shaft, self._color)
        mb.addPyramid(5, 5, 5, 0, Vector.Unit_Y, center_head, self._color)
        
        '''
        mat = Matrix()
        mat.setByRotationAxis(180*n.x, Vector.Unit_X)
        mat.setByRotationAxis(-180*(1-n.y), Vector.Unit_Y)
        mat.setByRotationAxis(180*n.z, Vector.Unit_Z)
        self._arrow.rotate(Quaternion().fromMatrix(mat))
        '''

        #  Add to Cura Scene
        self._arrow.setMeshData(mb.build())

    '''
      findCenter()

        calculates center vector for currently selected face
    '''
    def findCenter(self):
        i = 0
        x = 0.
        y = 0.
        z = 0.

        if self._tri is None:
            return [0, 0, 0]

        for p in self._tri.points:
            
            x += p.x
            y += p.y
            z += p.z
            
            i += 1

        return [x/i, y/i, z/i]


    def clearSelection(self):
        mb = MeshBuilder()
        self.setSolidMesh(mb.build())  

    def _onEngineCreated(self):
        self._connector._onEngineCreated()