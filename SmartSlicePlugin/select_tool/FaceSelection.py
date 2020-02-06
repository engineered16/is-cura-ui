# FaceSelection.py
# Teton Simulation
# Authored on   November  1, 2019
# Last Modified November 16, 2019

#
# Contains definitions for Cura Smart Slice Selectable Faces
#

'''
    SelectableFace are always in terms of Cura's coordinate system
    CalculatableFace are always in terms of PyWim's coordinate system
'''

from sys import float_info

#  STANDARD IMPORTS
from UM.Math.Vector import Vector
from UM.Math.AxisAlignedBox import AxisAlignedBox
import numpy

#  Ultimaker/Cura Imports
from UM.Math import NumPyUtil
from UM.Mesh import MeshData
from UM.Logger import Logger


''' 
  SelectableFace(points, normals)
    'points' is a list of Point_3(x, y, z)
    'normals' is an 'immutableNDArray' containing (x, y, z) components for point normal vectors

    Contains definition for a selectable face with normal vector
    
    NOTE:  'normals' is passed through for Cura  (UNUSED)
           'normals' will likely be used by CGAL (NOT DEPRECATED!!)
'''
class SelectableFace:
#  CONSTRUCTOR
    def __init__(self, face_id, points, normals):
        self._id = face_id
        self._points = points
        self._edges = self.generateEdges()
        self._normal = self.generateNormalVector()

        self._vert_normals = normals
        self._selected = False

    def __str__(self):
        return '{} :: {}, {}, {}'.format(self._id, self._points[0], self._points[1], self._points[2])

#  ACCESSORS

    def __eq__(self, other):
        '''
        Face equality is true if both faces have the same point ids, order does not need to be consistent
        '''
        pids = [p._id for p in self._points]
        oids = [p._id for p in other._points]
        for pid in pids:
            if pid not in oids:
                return False
        return True

    '''
      points()
        Returns list of Selectable Points
    '''
    @property
    def points(self):
        return self._points

    '''
      edges()
        Returns list of Selectable Edges
    '''
    @property
    def edges(self):
        return self._edges

    '''
      normal()
        Returns the FaceWithNormal's Normal Vector
    '''
    @property
    def normal(self):
        return self._normal

    '''
      vnormals()
        Returns the list of vertex normal vector
    '''
    @property
    def vnormals(self):
        return self._vert_normals

    '''  selected()
        Returns true if face is selected
                false otherwise
    '''
    @property
    def selected(self):
        return self._selected

    '''
      getPoint(i)
        Returns the PointWithNormal at index: i
    '''
    def getPoint(self, i):
        return self._points[i]

    ''' 
      printDetails()
        Gives a printout of meaningful properties regarding SelectableFace
    '''
    def printDetails(self):
        print ("# of Points:  " + str(len(self._points)))
        for p in self._points:
            print ("Point: (" + str(p.x()) + ", " + str(p.y()) + ", " + str(p.z()) + ")")
        print ("\n")


#  MUTATORS

    '''
      addPoint()
        If there is no conflict, adds PointWithNormal to FaceWithNormal
    '''
    def addPoint(self, point):
        self._points.append(point)

    '''
      select()
        Sets SelectableFace Selection status to True
    '''
    def select(self):
        self._selected = True

    '''
      deselect()
        Sets SelectableFace Selection status to False
    '''
    def deselect(self):
        self._selected = False

    '''
      addTri()
        Adds triangle to SelectableFace
    '''
    def addTri(self, tri):
        #  Add Points to Face if Necessary
        for p in tri.points:
            _add = True
            for q in self._points:
                #  If Vertex is already in face...
                if ((p.x() == q.x()) and (p.y() == q.y()) and (p.z() == q.z())):
                    _add = False
            if (_add):
                #  Add Point and Associated Edges to Face
                self.addPoint(p)
                for p2 in tri.points:
                    if (p != p2):
                        self.addEdge(p, p2)
        
  

    '''
      generatedEdges()
        Sets Facet edges to be the outline of the shape
    '''
    def generateEdges(self):
        #  ASSUMES STARTING FACET IS TRIANGLE FOR NOW
        edges = [SelectableEdge(self._points[0], self._points[1])]
        edges.append(SelectableEdge(self._points[1], self._points[2]))
        edges.append(SelectableEdge(self._points[2], self._points[0]))
        return edges

    def addEdge(self, p1, p2):
        self._edges.append(SelectableEdge(p1, p2))

    '''
      removeEdge(edge)
        If 'edge' is in the SelectableFace, remove it
    '''
    def removeEdge(self, edge):
        for e in self._edges:
            if ((edge.p1 == e.p1 and edge.p2 == e.p2) or (edge.p1 == e.p2 and edge.p2 == e.p1)):
                self._edges.remove(e)

    '''
      generateNormalVector()
        Returns the cross product of the first three points within the Face

        This makes the assumption that all other points beyond p3 are COPLANAR
    '''
    def generateNormalVector(self):
        vec1 = Vector(self._points[1].x - self._points[0].x, self._points[1].y - self._points[0].y, self._points[1].z - self._points[0].z)
        vec2 = Vector(self._points[2].x - self._points[0].x, self._points[2].y - self._points[0].y, self._points[2].z - self._points[0].z)
        cross_x = vec1.y*vec2.z - vec1.z*vec2.y
        cross_y = vec1.z*vec2.x - vec1.x*vec2.z
        cross_z = vec1.x*vec2.y - vec1.y*vec2.x
        mag   = numpy.sqrt((cross_x*cross_x) + (cross_y*cross_y) + (cross_z*cross_z))
        self._normal = Vector(cross_x/mag, cross_y/mag, cross_z/mag)
        return self._normal
     
    def isPointContained(self, point):
        """
        Check whether given point lies inside this selectable face.
        Inputs:
            point (SelectablePoint) is single point.
        Output:
            Boolean (bool) True means point lies within face. False means point is outside of face.
        Notes:
            The tolerance expansion near end makes this method not 100% accurate.
        """
        for i, p1 in enumerate(self._points[:-2]):
            p2 = self._points[i + 1]
            p3 = self._points[i + 2]
            
            area_2 = self.findArea(p1, p2, p3)
            alpha = self.findArea(point, p2, p3) / area_2
            beta = self.findArea(point, p3, p1) / area_2
            gama = self.findArea(point, p1, p2) / area_2
            
            total = gama + alpha + beta
            #This algorithm does not count line edge intersections.  Expand tolerance to include.
            return total > 0.99 and total < 1.01

    def findArea(self, p, q, r):
        """
        Finds area times two.
        Input:
            p1, p2, p3  (SelectablePoint) each is a 3D point.
        Output:
            (float) the area of triangle multiplied by 2.
        Notes:
            To get the actual area, the user must divide answer by 2!
        """
        pq = (q.x - p.x, q.y - p.y, q.z - p.z)
        pr = (r.x - p.x, r.y - p.y, r.z - p.z)
        vect = numpy.cross(pq, pr)
        area_2 = numpy.sqrt(vect[0]**2 + vect[1]**2 + vect[2]**2)
        return area_2

'''
  SelectableEdge(p1, p2)
    'p1' and 'p2' are 'SelectablePoint'

    Edges denote lines between two vertices in 3D space
'''
class SelectableEdge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
        self._selected = False


'''
  SelectablePoint(x, y, z, normals)
    'x', 'y', and 'z' are floating point coordinates
    'normals' is an immutableNDArray containing normal vectors for each vertex

    NOTE:  'normals' is passed through for Cura  (UNUSED)
           'normals' will likely be used by CGAL (NOT DEPRECATED!!)
'''
class SelectablePoint:
#  CONSTRUCTORS
    def __init__(self, point_id, x, y, z, normals):
        self._p = Vector(x, y, z)
        self._normals = normals

        self._selected = False

        self._id = point_id

    def __str__(self):
        return '[{}, {}, {}]'.format(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neq__(self, other):
        return self.x != other.x or self.y != other.y or self.z != other.z

#  ACCESSORS

    '''
      x()
        Returns value of SelectablePoint x coordinate component
    '''
    @property
    def x(self):
        return self._p.x

    '''
      y()
        Returns value of SelectablePoint y coordinate component
    '''
    @property
    def y(self):
        return self._p.y

    '''
      z()
        Returns value of SelectablePoint z coordinate component
    '''
    @property
    def z(self):
        return self._p.z


#  MUTATORS 

    '''
      x(new_x)
        'new_x' is a floating point value

        Sets SelectablePoint x coordinate component to 'new_x'
    '''
    @x.setter
    def x(self, new_x):
        self._p.x(new_x)

    '''
      y(new_y)
        'new_y' is a floating point value

        Sets SelectablePoint x coordinate component to 'new_y'
    '''
    @y.setter
    def y(self, new_y):
        self._p.y(new_y)

    '''
      z(new_z)
        'new_z' is a floating point value

        Sets SelectablePoint x coordinate component to 'new_z'
    '''
    @z.setter
    def z(self, new_z):
        self._p.z(new_z)


#
# CONVENIENCE UTILITIES
#

'''
  toCalculatablePoint(p)
    p: SelectablePoint
'''
def toCalculatablePoint(p):
    n = p._normals
    return SelectablePoint(0, p.x, -p.z, p.y, [n[0], -n[2], n[1]])

def toCalculatableFace(f):
    p = f.points
    
    p0 = toCalculatablePoint(p[0])
    p1 = toCalculatablePoint(p[1])
    p2 = toCalculatablePoint(p[2])

    ns = [p0._normals, p1._normals, p2._normals]

    return SelectableFace(0, [p0, p1, p2], ns)

'''
  fromCalculatablePoint(x, y,  z)
    x, y, z : real numbers
'''
def fromCalculatablePoint(x, y, z, vnormals=[[],[],[]]):
    return SelectablePoint(x, z, -y, vnormals)


'''
  fromCalculatableFace(points, normals)
'''
def fromCalculatableFace(points, normals=[]):
    return SelectableFace(points, normals)

class SelectableMesh:
    def __init__(self, mesh_data):
        self.points = dict()
        self.faces = dict()
        

        nfaces = int(len(mesh_data._vertices) / 3)

        if mesh_data._indices is not None and len(mesh_data._indices) > 0:
            indices = mesh_data._indices
        else:
            indices = None

        vertices = mesh_data._vertices
        normals = mesh_data._normals

        v0 = vertices[0]

        minv = Vector(v0[0], v0[1], v0[2])
        maxv = Vector(v0[0], v0[1], v0[2])

        for v in vertices:
            x, y, z = v[0:3]
            minv = minv.set(min(x, minv.x), min(y, minv.y), min(z, minv.z))
            maxv = maxv.set(max(x, maxv.x), max(y, maxv.y), max(z, maxv.z))

        self.box = AxisAlignedBox(minimum=minv, maximum=maxv)

        for f in range(nfaces):
            if indices is not None:
                i, j, k = indices[f][0:3]
            else:
                base_index = f * 3
                i = base_index
                j = base_index + 1
                k = base_index + 2

            v_a = vertices[i]
            v_b = vertices[j]
            v_c = vertices[k]

            n_a = normals[i]
            n_b = normals[j]
            n_c = normals[k]

            p_a = self.getOrAddPoint(v_a, n_a)
            p_b = self.getOrAddPoint(v_b, n_b)
            p_c = self.getOrAddPoint(v_c, n_c)

            face = SelectableFace(len(self.faces), [p_a, p_b, p_c], [n_a, n_b, n_c])

            self.faces[face._id] = face

    def getOrAddPoint(self, vertex, normal) -> SelectablePoint:
        '''
        Retrieves a point if it already exists, else it is added and returns
        '''
        point = SelectablePoint(0, float(vertex[0]), float(vertex[1]), float(vertex[2]), normal)

        for pid in self.points.keys():
            if self.points[pid] == point: # checks coordinate equality
                return self.points[pid]

        # does not exist, add it
        point._id = len(self.points)
        self.points[point._id] = point

        return point   
