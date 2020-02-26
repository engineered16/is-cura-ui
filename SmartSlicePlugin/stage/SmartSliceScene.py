from typing import List

from UM.Logger import Logger
from UM.Mesh.MeshBuilder import MeshBuilder
from UM.Math.Color import Color
from UM.Math.Vector import Vector
from UM.Scene.SceneNode import SceneNode

from cura.CuraApplication import CuraApplication
from cura.Scene.CuraSceneNode import CuraSceneNode

from ..utils import makeInteractiveMesh

import pywim
import numpy

class Root(SceneNode):
    def __init__(self):
        super().__init__(name='_SmartSlice', visible=True)

        self._interactive_mesh = None

        self.anchor_face = None # AnchorFace
        self.load_face = None # LoadFace

    def initialize(self, parent : SceneNode):
        parent.addChild(self)

        mesh_data = parent.getMeshData()

        if mesh_data:
            Logger.log('d', 'Compute interactive mesh from SceneNode {}'.format(parent.getName()))

            self._interactive_mesh = makeInteractiveMesh(mesh_data)

    def getInteractiveMesh(self) -> pywim.geom.tri.Mesh:
        return self._interactive_mesh

class HighlightFace(SceneNode):
    def __init__(self, name : str):
        super().__init__(name=name, visible=True)

        self._triangles = []

    def _annotatedMeshData(self, mb : MeshBuilder):
        pass

    def setMeshDataFromPywimTriangles(self, tris : List[pywim.geom.tri.Triangle]):
        self._triangles = tris

        mb = MeshBuilder()

        for tri in self._triangles:
            mb.addFace(tri.v1, tri.v2, tri.v3)

        self._annotatedMeshData(mb)

        mb.calculateNormals()

        self.setMeshData(mb.build())

class AnchorFace(HighlightFace):
    pass

class LoadFace(HighlightFace):
    def __init__(self, name : str):
        super().__init__(name)

        self._invert_arrow = False

        self._arrow_head_length = 8
        self._arrow_tail_length = 22
        self._arrow_total_length = self._arrow_head_length + self._arrow_tail_length
        self._arrow_head_width = 2.8
        self._arrow_tail_width = 0.8

    def setArrowDirection(self, inverted):
        self._invert_arrow = inverted
        self.setMeshDataFromPywimTriangles(self._triangles)

    def _annotatedMeshData(self, mb : MeshBuilder):
        """
        Draw an arrow to the normal of the given face mesh using MeshBuilder.addFace().
        Inputs:
            tris (list of faces or triangles) Only one face will be used to begin arrow.
            mb (MeshBuilder) which is drawn onto.
        """
        if len(self._triangles) <= 0: # input list is empty
            return

        index = len(self._triangles) // 2
        tri = self._triangles[index]
        #p = tri.points
        #tri.generateNormalVector()
        n = tri.normal
        n = Vector(n.r, n.s, n.t) # pywim Vector to UM Vector
        #invert_arrow = self._connector._proxy.loadDirection
        center = self.findFaceCenter(self._triangles)
        
        p_base0 = Vector(center.x + n.x * self._arrow_head_length,
                         center.y + n.y * self._arrow_head_length,
                         center.z + n.z * self._arrow_head_length)
        p_tail0 = Vector(center.x + n.x * self._arrow_total_length,
                         center.y + n.y * self._arrow_total_length,
                         center.z + n.z * self._arrow_total_length)
        
        if self._invert_arrow:
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
        
        mb.addFace(p_base1, p_head, p_base3)
        mb.addFace(p_base3, p_head, p_base2)
        mb.addFace(p_base2, p_head, p_base4)
        mb.addFace(p_base4, p_head, p_base1)
        mb.addFace(p_base5, p_head, p_base1)
        mb.addFace(p_base6, p_head, p_base1)
        mb.addFace(p_base6, p_head, p_base2)
        mb.addFace(p_base2, p_head, p_base5)
        mb.addFace(p_base3, p_head, p_base5)
        mb.addFace(p_base5, p_head, p_base4)
        mb.addFace(p_base4, p_head, p_base6)
        mb.addFace(p_base6, p_head, p_base3)
        
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
        
        mb.addFace(p_tail1, p_tail_base1, p_tail3)
        mb.addFace(p_tail3, p_tail_base3, p_tail2)
        mb.addFace(p_tail2, p_tail_base2, p_tail4)
        mb.addFace(p_tail4, p_tail_base4, p_tail1)
        mb.addFace(p_tail5, p_tail_base5, p_tail1)
        mb.addFace(p_tail6, p_tail_base6, p_tail1)
        mb.addFace(p_tail6, p_tail_base6, p_tail2)
        mb.addFace(p_tail2, p_tail_base2, p_tail5)
        mb.addFace(p_tail3, p_tail_base3, p_tail5)
        mb.addFace(p_tail5, p_tail_base5, p_tail4)
        mb.addFace(p_tail4, p_tail_base4, p_tail6)
        mb.addFace(p_tail6, p_tail_base6, p_tail3)
        
        mb.addFace(p_tail_base1, p_tail_base3, p_tail3)
        mb.addFace(p_tail_base3, p_tail_base2, p_tail2)
        mb.addFace(p_tail_base2, p_tail_base4, p_tail4)
        mb.addFace(p_tail_base4, p_tail_base1, p_tail1)
        mb.addFace(p_tail_base5, p_tail_base1, p_tail1)
        mb.addFace(p_tail_base6, p_tail_base1, p_tail1)
        mb.addFace(p_tail_base6, p_tail_base2, p_tail2)
        mb.addFace(p_tail_base2, p_tail_base5, p_tail5)
        mb.addFace(p_tail_base3, p_tail_base5, p_tail5)
        mb.addFace(p_tail_base5, p_tail_base4, p_tail4)
        mb.addFace(p_tail_base4, p_tail_base6, p_tail6)
        mb.addFace(p_tail_base6, p_tail_base3, p_tail3)

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
            if LoadFace._triangleContainsPoint(tri, c_point):
                return c_point
        
        # When center point is not on face, choose instead center point of middle triangle.
        index = len(triangles) // 2
        tri = triangles[index]
        return self.findPointsCenter(tri.points)

    @staticmethod
    def _triangleContainsPoint(triangle, point):
        v1 = triangle.v1
        v2 = triangle.v2
        v3 = triangle.v3

        area_2 = LoadFace._threePointArea2(v1, v2, v3)
        alpha = LoadFace._threePointArea2(point, v2, v3) / area_2
        beta = LoadFace._threePointArea2(point, v3, v1) / area_2
        gamma = LoadFace._threePointArea2(point, v1, v2) / area_2

        total = alpha + beta + gamma

        return total > 0.99 and total < 1.01
    
    @staticmethod
    def _threePointArea2(p, q, r):
        pq = (q.x - p.x, q.y - p.y, q.z - p.z)
        pr = (r.x - p.x, r.y - p.y, r.z - p.z)

        vect = numpy.cross(pq, pr)

        # Return area X 2
        return numpy.sqrt(vect[0]**2 + vect[1]**2 + vect[2]**2)

