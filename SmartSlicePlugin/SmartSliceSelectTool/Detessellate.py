# Detessellate.py
# Teton Simulation
# Authored on   October 31, 2019
# Last Modified October 31, 2019

#
# Contains functionality for converting a tessellated (TRIANGLES)
# irregular polyhedron into a set of facets
#


import math

#  UM/Cura Imports
from UM.Math.Vector import Vector

from .FaceSelection import SelectableFace

'''
  detessellate(tris)
    Converts list of triangles into list of polygons

    A set of triangles are considered a polygon if:
      *  All triangles are COPLANAR
      *  All triangles are Recursively Jointed on two vertices 
'''
def detessellate(tris):
    #  Initialize Face Buffer
    _faces = []

    #  Iterate for every triangle
    for tri in tris:
        _added = False
        #  Check against detected Faces
        for face in _faces:
            #  If both jointed/coplanar, add tri to face
            if (isJointed(tri, face) and isCoplanar(tri, face)):
                face.addTri(tri)
                _added = True

                #  THEN....
                #  Check for other shapes that could be jointed with this one
                break
        if (not _added):
            _faces.append(tri)

    return _faces


#
#   HELPER FUNCTIONS
#

'''
  isJointed(face1, face2)
    Returns TRUE if 'face1' and 'face2' share at least 2 vertices
'''
def isJointed(face1, face2):
    matched = 0
    for p in face1.points:
        for q in face2.points:
            #if ((p.x == q.x) and (p.y == q.y) and (p.z == q.z)):
            if p._id == q._id:
                matched += 1
                if (matched >= 2):
                    return True
    return False

'''
  isCoplanar(face1, face2)
    Returns TRUE if 'face1' and 'face2' share the same normal vector
'''
def isCoplanar(face1, face2):
    return face1.normal.angleToVector(face2.normal) < 0.01 # roughly 0.57 degrees
        
    #if ((face1.normal.x == face2.normal.x) and (face1.normal.y == face2.normal.y) and (face1.normal.z == face2.normal.z)):
    #    return True
    #return False


