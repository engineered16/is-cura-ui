# SmartSliceSelectHandle.py
# Teton Simulation
# Last Modified November 12, 2019

# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.

#
#   Contains functionality to be triggered upon face selection
#

import time

#  UM/Cura Imports
from UM.Logger import Logger
from UM.Scene.ToolHandle import ToolHandle
from UM.Scene.SceneNode import SceneNode
from UM.Mesh.MeshBuilder import MeshBuilder
from UM.Mesh.MeshData import MeshData
from UM.PluginRegistry import PluginRegistry

from UM.Math.Color import Color
from UM.Math.Matrix import Matrix
from UM.Math.Quaternion import Quaternion
from UM.Math.Vector import Vector

# Provides enums
class SelectionMode:
    AnchorMode = 1
    LoadMode = 2

class SmartSliceSelectHandle(ToolHandle):
#  CONSTRUCTORS
    def __init__(self, extension, parent = None, tri = None):
        super().__init__(parent)

        self._name = "SmartSliceSelectHandle"
        self._connector = extension.cloud # SmartSliceCloudConnector

        #  Default Line Properties
        self._edge_width = 0.8
        self._edge_length = [] # TODO: GET THIS FROM FACE EDGES
        self._selected_color = Color(0, 0, 255, 255)
        self._anchored_color = self._y_axis_color
        self._loaded_color = self._y_axis_color

        #  Selected Face Properties
        self._tri = tri
        self._face = []
        #  Previously Selected Faces
        self._loaded_faces = []
        self._load_magnitude = 0
        self._anchored_faces = []

        #  For Performance
        self._has_anchor = False
        self._has_loads  = False

        #   Arrow Mesh
        self._arrow = False
        self._arrow_head_length = 8
        self._arrow_tail_length = 22
        self._arrow_total_length = self._arrow_head_length + self._arrow_tail_length
        self._arrow_head_width = 2.8
        self._arrow_tail_width = 0.8
        
        #  Disable auto scale
        self._auto_scale = False

        self._connector.SmartSlicePrepared.connect(self._onSmartSlicePrepared)


    def _onSmartSlicePrepared(self):
        #  Connect to UI 'Cancel Changes' Signal
        self._connector.propertyHandler.selectedFacesChanged.connect(self.drawSelection)
        self._connector.propertyHandler._selection_mode = SelectionMode.LoadMode
        self._connector._proxy.loadDirectionChanged.connect(self.drawSelection)


#  ACCESSORS
    @property
    def face(self):
        return self._tri

#  MUTATORS
    def setFace(self, f):
        self._tri = f

    #def getLoadVector(self) -> Vector:
    #    if len(self._loaded_faces) > 0:
    #        load_mag = self._connector._proxy._loadMagnitude
    #        if self._connector._proxy.loadDirection:
    #            load_mag *= -1
    #        n = self._loaded_faces[0].normal * load_mag
    #        return Vector(n.r, n.s, n.t)
    #    return Vector(0., 0., 0.) # no load face available to determine vector

    '''
      drawSelection()

        Uses UM's MeshBuilder to construct 3D Arrow mesh and translates/rotates as to be normal to the selected face
    '''
    def drawSelection(self):
        if self._tri is None:
            return

        #  Construct Edges using MeshBuilder Cubes
        mb = MeshBuilder()
        #_selected_mesh = None

        #Logger.log("d", "Root Face: {}".format(self._tri))

        Logger.log("d", "Drawing Face Selection")

        #if self._connector.propertyHandler._selection_mode == SelectionMode.LoadMode:
            #self._load_magnitude = self._connector._proxy._loadMagnitude
            #_selected_mesh = self._connector.propertyHandler._loadedMesh
            #  TODO: Generalize this for more than one Active Load
            # TODO-BRADY Commented below out - what is it for?
            #if self._connector.propertyHandler._loadedFaces[0] is not None:
            #    self.setFace(self._connector.propertyHandler._loadedFaces[0])
        #else:
            #_selected_mesh = self._connector.propertyHandler._anchoredMesh
            #  TODO: Generalize this for more than one Active Anchor
            # TODO-BRADY Commented below out - what is it for?
            #if self._connector.propertyHandler._anchoredFaces[0] is not None:
            #    self.setFace(self._connector.propertyHandler._anchoredFaces[0])
        
        # TODO-BRADY - is self._face used for anything?
        #self._face = set()

        for tri in self._tri:
            mb.addFace(tri.v1, tri.v2, tri.v3, color=self._selected_color)

        if self._connector.propertyHandler._selection_mode == SelectionMode.LoadMode:
            self._load_magnitude = self._connector._proxy._loadMagnitude
            #self._loaded_faces = self._tri
            #self._connector.propertyHandler._selection_mode = SelectionMode.LoadMode
            self.paintArrow(self._tri, mb)
        #else:
            #self._anchored_faces = self._tri
            #self._connector.propertyHandler._selection_mode = SelectionMode.AnchorMode

        #  Add to Cura Scene
        self.setSolidMesh(mb.build())

        #Logger.log("d", "Anchor Faces: {}".format([f._id for f in self._anchored_faces]))
        #Logger.log("d", "Load Faces: {}".format([f._id for f in self._loaded_faces]))
        #Logger.log("d", "Load Vector: {}".format(self.getLoadVector()))


    def paintArrow(self, face_list, mb):
        """
        Draw an arrow to the normal of the given face mesh using MeshBuilder.addFace().
        Inputs:
            face_list (list of faces or triangles) Only one face will be used to begin arrow.
            mb (MeshBuilder) which is drawn onto.
        """
        if len(face_list) <= 0: # input list is empty
            return
        index = len(face_list) // 2
        tri = face_list[index]
        #p = tri.points
        #tri.generateNormalVector()
        n = tri.normal
        n = Vector(n.r, n.s, n.t) # pywim Vector to UM Vector
        invert_arrow = self._connector._proxy.loadDirection
        center = self.findFaceCenter(face_list)
        
        p_base0 = Vector(center.x + n.x * self._arrow_head_length,
                         center.y + n.y * self._arrow_head_length,
                         center.z + n.z * self._arrow_head_length)
        p_tail0 = Vector(center.x + n.x * self._arrow_total_length,
                         center.y + n.y * self._arrow_total_length,
                         center.z + n.z * self._arrow_total_length)
        
        if invert_arrow:
            p_base0 = Vector(center.x + n.x * self._arrow_tail_length,
                             center.y + n.y * self._arrow_tail_length,
                             center.z + n.z * self._arrow_tail_length)
            p_head = p_tail0
            p_tail0 = center
        else:   # regular
            p_head = center

        p_base1 = Vector(p_base0.x, p_base0.y + self._arrow_head_width, p_base0.z)
        p_base2 = Vector(p_base0.x, p_base0.y - self._arrow_head_width, p_base0.z)
        p_base3 = Vector(p_base0.x + self._arrow_head_width, p_base0.y, p_base0.z)
        p_base4 = Vector(p_base0.x - self._arrow_head_width, p_base0.y, p_base0.z)
        p_base5 = Vector(p_base0.x, p_base0.y, p_base0.z + self._arrow_head_width)
        p_base6 = Vector(p_base0.x, p_base0.y, p_base0.z - self._arrow_head_width)
        
        mb.addFace(p_base1, p_head, p_base3, color=self.YAxisSelectionColor)
        mb.addFace(p_base3, p_head, p_base2, color=self.YAxisSelectionColor)
        mb.addFace(p_base2, p_head, p_base4, color=self.YAxisSelectionColor)
        mb.addFace(p_base4, p_head, p_base1, color=self.YAxisSelectionColor)
        mb.addFace(p_base5, p_head, p_base1, color=self.YAxisSelectionColor)
        mb.addFace(p_base6, p_head, p_base1, color=self.YAxisSelectionColor)
        mb.addFace(p_base6, p_head, p_base2, color=self.YAxisSelectionColor)
        mb.addFace(p_base2, p_head, p_base5, color=self.YAxisSelectionColor)
        mb.addFace(p_base3, p_head, p_base5, color=self.YAxisSelectionColor)
        mb.addFace(p_base5, p_head, p_base4, color=self.YAxisSelectionColor)
        mb.addFace(p_base4, p_head, p_base6, color=self.YAxisSelectionColor)
        mb.addFace(p_base6, p_head, p_base3, color=self.YAxisSelectionColor)
        
        p_tail1 = Vector(p_tail0.x, p_tail0.y + self._arrow_tail_width, p_tail0.z)
        p_tail2 = Vector(p_tail0.x, p_tail0.y - self._arrow_tail_width, p_tail0.z)
        p_tail3 = Vector(p_tail0.x + self._arrow_tail_width, p_tail0.y, p_tail0.z)
        p_tail4 = Vector(p_tail0.x - self._arrow_tail_width, p_tail0.y, p_tail0.z)
        p_tail5 = Vector(p_tail0.x, p_tail0.y, p_tail0.z + self._arrow_tail_width)
        p_tail6 = Vector(p_tail0.x, p_tail0.y, p_tail0.z - self._arrow_tail_width)
        
        p_tail_base1 = Vector(p_base0.x, p_base0.y + self._arrow_tail_width, p_base0.z)
        p_tail_base2 = Vector(p_base0.x, p_base0.y - self._arrow_tail_width, p_base0.z)
        p_tail_base3 = Vector(p_base0.x + self._arrow_tail_width, p_base0.y, p_base0.z)
        p_tail_base4 = Vector(p_base0.x - self._arrow_tail_width, p_base0.y, p_base0.z)
        p_tail_base5 = Vector(p_base0.x, p_base0.y, p_base0.z + self._arrow_tail_width)
        p_tail_base6 = Vector(p_base0.x, p_base0.y, p_base0.z - self._arrow_tail_width)
        
        mb.addFace(p_tail1, p_tail_base1, p_tail3, color=self.YAxisSelectionColor)
        mb.addFace(p_tail3, p_tail_base3, p_tail2, color=self.YAxisSelectionColor)
        mb.addFace(p_tail2, p_tail_base2, p_tail4, color=self.YAxisSelectionColor)
        mb.addFace(p_tail4, p_tail_base4, p_tail1, color=self.YAxisSelectionColor)
        mb.addFace(p_tail5, p_tail_base5, p_tail1, color=self.YAxisSelectionColor)
        mb.addFace(p_tail6, p_tail_base6, p_tail1, color=self.YAxisSelectionColor)
        mb.addFace(p_tail6, p_tail_base6, p_tail2, color=self.YAxisSelectionColor)
        mb.addFace(p_tail2, p_tail_base2, p_tail5, color=self.YAxisSelectionColor)
        mb.addFace(p_tail3, p_tail_base3, p_tail5, color=self.YAxisSelectionColor)
        mb.addFace(p_tail5, p_tail_base5, p_tail4, color=self.YAxisSelectionColor)
        mb.addFace(p_tail4, p_tail_base4, p_tail6, color=self.YAxisSelectionColor)
        mb.addFace(p_tail6, p_tail_base6, p_tail3, color=self.YAxisSelectionColor)
        
        mb.addFace(p_tail_base1, p_tail_base3, p_tail3, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base3, p_tail_base2, p_tail2, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base2, p_tail_base4, p_tail4, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base4, p_tail_base1, p_tail1, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base5, p_tail_base1, p_tail1, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base6, p_tail_base1, p_tail1, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base6, p_tail_base2, p_tail2, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base2, p_tail_base5, p_tail5, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base3, p_tail_base5, p_tail5, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base5, p_tail_base4, p_tail4, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base4, p_tail_base6, p_tail6, color=self.YAxisSelectionColor)
        mb.addFace(p_tail_base6, p_tail_base3, p_tail3, color=self.YAxisSelectionColor)

    def findPointsCenter(self, points):
        """
            Find center point among all input points.
            Input:
                points   (list) a list of one or more pywim.geom.Vertex points.
            Output: (Vector) A single vector averaging the input points.
        """
        xs = 0
        ys = 0
        zs = 0
        for p in points:
            xs += p.x
            ys += p.y
            zs += p.z
        num_p = len(points)
        return Vector(xs / num_p, ys / num_p, zs / num_p)

    def findFaceCenter(self, triangles):
        """
            Find center of face.  Return point is guaranteed to be on face.
            Inputs:
                triangles: (list) Triangles. All triangles assumed to be in same plane.
        """
        c_point = self.findPointsCenter([point for tri in triangles for point in tri.points]) # List comprehension creates list of points.
        for tri in triangles:
            # TODO-BRADY
            #if tri.isPointContained(c_point):
            if True:
                return c_point
        
        # When center point is not on face, choose instead center point of middle triangle.
        index = len(triangles) // 2
        tri = triangles[index]
        return self.findPointsCenter(tri.points)

    def clearSelection(self):
        self.setSolidMesh(MeshBuilder().build())  


