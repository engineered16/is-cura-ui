# SmartSliceModifierMesh.py
# Teton Simulation
# Authored on   November 16, 2019
# Last Modified November 16, 2019

#
# Cura  for Smart Slice Plugin's *intelligent* Modifer Mesh
#


#  PyWim Imports
from pywim.smartslice.result import Result
from pywim.chop import mesh


#  Cura's Imports
from UM.Application import Application
from UM.Signal import Signal

from UM.Settings.SettingInstance import SettingInstance
from cura.Settings.SettingOverrideDecorator import SettingOverrideDecorator

from UM.Math.Vector import Vector

from UM.Mesh.MeshData import MeshData
from UM.Mesh.MeshBuilder import MeshBuilder

from UM.Scene.SceneNode import SceneNode

#  Local Imports
from .PreviewModifierMesh import PreviewModifierMesh


class SmartSliceModifierMesh(SceneNode):

#  CONSTRUCTORS
    
    '''
      SmartSliceModifierMesh(result_mesh)
        result_mesh: PyWim Mesh 

        Each SmartSliceModifierMesh is a MeshData with 'ModifierMesh' attributes.
        These are affected by factors such as DENSITY and PATTERN.
    '''
    def __init__(self, result_mesh=None):
        super().__init__()

        #   Connect Modifier Mesh to Cura Application
        Application.getInstance().engineCreatedSignal.connect(self._engineCreated)
        
        #   Get Reference to Controller
        self._controller = Application.getInstance().getController()
        self._id = 0
        self._version = 0
        self._meta_data = None

        #  Initialize Modifier Mesh Properties
        self._pattern = None
        self._density = 0.
        self._pmm = PreviewModifierMesh(self)
        self.addInfillProperty()

        #  Lists of Faces/Vertices for Reference
        self._faces = []
        self._verts = []

        #  Signal Connections
        #       Emits a Signal when the infill MeshData changes
        self.meshPropertiesChanged = Signal()
        '''
            TODO:  connect PreviewModifierMesh to 'Preview' button signal in SmartSliceStage

             ***.connect(self._pmm.preview())
        '''

    def _engineCreated(self):
        1 + 1 #  STUB


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
      addInfillProperty()

        Sets this SceneNode's mesh attribute to exclusively 'infill_mesh'
    '''
    def addInfillProperty(self):
        #  Add Settings Override Decorator to this SceneNode
        #       This can be used to override the infill thread density
        stack = self.callDecoration("getStack")
        if not stack:
            self.addDecorator(SettingOverrideDecorator())
            stack = self.callDecoration("getStack")

        #  Get Settings for this Modifier Mesh
        settings = stack.getTop()

        #  Set mesh properties exclusively to 'infill_mesh'
        for property_key in ["infill_mesh", "cutting_mesh", "support_mesh", "anti_overhang_mesh"]:
            if property_key != "infill_mesh":
                if settings.getInstance(property_key):
                    settings.removeInstance(property_key)
            else:
                if not (settings.getInstance(property_key) and settings.getProperty(property_key, "value")):
                    definition = stack.getSettingDefinition(property_key)
                    new_instance = SettingInstance(definition, settings)
                    new_instance.setProperty("value", True)
                    new_instance.resetState()  # Ensure that the state is not seen as a user state.
                    settings.addInstance(new_instance)


    '''
      getMesh(_mesh)
        _mesh: PyWim Mesh

        Returns a MeshData object for Cura/UM libraries, which
            corresponds to the given PyWim Mesh
    '''
    def getCuraMesh(self, _mesh: mesh.Mesh):
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

        #  Build a Cura MeshData object from PyWim Result and set SceneNode's MeshData
        if _mesh is not None:
            md = self.getCuraMesh(_mesh)
            self.setMeshData(md)

        #  Notify listeners that the infill MeshData has changed
        self.meshPropertiesChanged.emit()

        # FOR DEBUGGING: Return Mesh_data
        return mesh_data
        

  #  Cura Plugin Overrides
    def setVersion(self, ver):
        self._version = ver

    def setMetaData(self, md):
        self._meta_data = md

    def setPluginId(self, _id):
        self._id = _id

