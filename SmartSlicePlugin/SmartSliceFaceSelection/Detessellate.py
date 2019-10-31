# Detessellate.py
# Teton Simulation
# Authored on   October 31, 2019
# Last Modified October 31, 2019

#
# Contains functionality for converting a tessellated (TRIANGLES)
# irregular polyhedron into a set of facets
#


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
        jointed  = False
        coplanar = False
        #  Check against detected Faces
        for face in _faces:
            #  Check if tri is jointd with face
            1 + 1 #STUB

            #  Check if tri is coplanar with face

        if ((not jointed) or (not coplanar)):
            _faces.append(tri)

    return _faces




