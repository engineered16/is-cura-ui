# SmartSliceModifierMesh.py
# Teton Simulation
# Authored on   November 16, 2019
# Last Modified November 16, 2019

#
# Cura  for Smart Slice Plugin's *intelligent* Modifer Mesh
#


from .py3mf.threemf.mesh import mesh

#  Cura's Imports
from UM.Mesh.MeshData import MeshData
from UM.Mesh.MeshBuilder import MeshBuilder

from UM.Math.Vector import Vector

#  Local Imports
from .FaceSelection import SelectableFace
from .FaceSelection import   toCalculatablePoint,   toCalculatableFace
from .FaceSelection import fromCalculatablePoint, fromCalculatableFace


class SmartSliceModifierMesh(MeshData):

#  CONSTRUCTORS
    
    '''
      SmartSliceModifierMesh()

        Each SmartSliceModifierMesh is a MeshData with 'ModifierMesh' attributes.
        These are affected by factors such as DENSITY and PATTERN.
    '''
    def __init__(self):
        super().__init__()

        #  Initialize Modifier Mesh Properties
        self._pattern = None
        self._density = 0.

        self._faces = []
        self._verts = []




#  ACCESSORS

    '''
      pattern()
        Returns instanced SmartSliceModifierMesh's pattern
    '''
    @property
    def pattern(self):
        return self._pattern

    '''
      density()
        Returns instanced SmartSliceModifierMesh's density
    '''
    @property
    def density(self):
        return self._density


#  MUTATORS
    @pattern.setter
    def pattern(self, new_pattern):
        self._pattern = new_pattern

    '''
      density(new_density)
        new_density: Real Number

        Sets the instanced SmartSliceModifierMesh's density to provided floating point number
    '''
    @density.setter
    def density(self, new_density: float):
        self._density = new_density


    '''
      getMesh(_mesh)
        _mesh: PyWim Mesh

        Populates SmartSliceModifierMesh (inherits MeshData) data with PyWim result mesh
    '''
    def getMesh(self, _mesh):
        '''
        TODO: Get CalculatablePoints and CalculatableFaces from PyWim
        '''
        mb = MeshBuilder()

        _tris = _mesh.triangles
        _verts = _mesh.vertices
        
        #  Iterate through all Triangles in Mesh
        for i in range(0, len(_tris)):
            
            #  Convert from PyWim -> Cura Coordinates
            p0 = _verts[3*i+0]
            p1 = _verts[3*i+2]
            p2 = -_verts[3*i+1]

            _face = _tris[i]

            #  Produce MeshData from faces in MeshBuilder
            mb.addFace(p0, p1, p2)

        #  Build meshes into a MeshData Object
        mesh_data = mb.build()
        
        #  TODO: Add 'Modifier Mesh' attribute


        # FOR DEBUGGING: Return Mesh_data
        return mesh_data
        
        
        


