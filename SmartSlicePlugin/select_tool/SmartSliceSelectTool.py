#  Ultimaker Imports
from UM.i18n import i18nCatalog

from UM.Application import Application
from UM.Version import Version
from UM.PluginRegistry import PluginRegistry
from UM.Logger import Logger
from UM.Event import Event, MouseEvent, KeyEvent
from UM.Tool import Tool
from UM.Math.Vector import Vector
from UM.Signal import Signal

from UM.View.GL.OpenGL import OpenGL
from UM.Scene.Selection import Selection
from UM.Scene.SceneNode import SceneNode

from cura.Scene.CuraSceneNode import CuraSceneNode

#  QT / QML Imports
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtQml import QQmlComponent, QQmlContext # @UnresolvedImport

#  Local Imports
from ..utils import makeInteractiveMesh
from ..SmartSliceExtension import SmartSliceExtension
from .SmartSliceSelectHandle import SelectionMode
from .SmartSliceSelectHandle import SmartSliceSelectHandle

i18n_catalog = i18nCatalog("smartslice")

##  Provides the tool to rotate meshes and groups
#
#   The tool exposes a ToolHint to show the rotation angle of the current operation
class SmartSliceSelectTool(Tool):
    def __init__(self, extension : SmartSliceExtension):
        super().__init__()
        self.extension = extension
        self._handle = SmartSliceSelectHandle(self.extension)

        #self._shortcut_key = Qt.Key_S

        self.setExposedProperties("AnchorSelectionActive",
                                  "LoadSelectionActive",
                                  "SelectionMode",
                                  )

        Selection.selectedFaceChanged.connect(self._onSelectedFaceChanged)

        self._scene = self.getController().getScene()
        self._scene_node_name = None
        self._interactive_mesh = None # pywim.geom.tri.Mesh
        self._load_face = None
        self._anchor_face = None

        self._controller.activeToolChanged.connect(self._onActiveStateChanged)

    ##  Handle mouse and keyboard events
    #
    #   \param event type(Event)
    def event(self, event):
        return super().event(event)

    def _calculateMesh(self):
        scene = Application.getInstance().getController().getScene()
        nodes = Selection.getAllSelectedObjects()

        if len(nodes) > 0:
            sn = nodes[0]
            #self._handle._connector._proxy._activeExtruderStack = nodes[0].callDecoration("getExtruderStack")

            if self._scene_node_name is None or sn.getName() != self._scene_node_name:

                mesh_data = sn.getMeshData()

                if mesh_data:
                    Logger.log('d', 'Compute interactive mesh from SceneNode {}'.format(sn.getName()))
                    
                    self._scene_node_name = sn.getName()
                    self._interactive_mesh = makeInteractiveMesh(mesh_data)
                    self._load_face = None
                    self._anchor_face = None

                    self._handle.clearSelection()
                    self._handle._connector._proxy._anchorsApplied = 0
                    self._handle._connector._proxy._loadsApplied = 0
                    self.extension.cloud._onApplicationActivityChanged()

                    controller = Application.getInstance().getController()
                    camTool = controller.getCameraTool()
                    aabb = sn.getBoundingBox()
                    if aabb:
                        camTool.setOrigin(aabb.center)

    def _onSelectedFaceChanged(self, curr_sf=None):
        if not self.getEnabled():
            return

        curr_sf = Selection.getSelectedFace()
        if curr_sf is None:
            return

        self._calculateMesh()

        scene_node, face_id = curr_sf

        self._handle._connector.propertyHandler.onSelectedFaceChanged(scene_node, face_id)

        #self.setFaceVisible(scene_node, face_id)

    def setFaceVisible(self, scene_node, face_id):
        ph = self._handle._connector.propertyHandler
        
        if self.getAnchorSelectionActive():
            self._handle._arrow = False
            self._anchor_face = (ph._anchoredNode, ph._anchoredID)
            self._handle.setFace(ph._anchoredTris)

        else:
            self._handle._arrow = True
            self._load_face = (ph._loadedNode, ph._loadedID)
            self._handle.setFace(ph._loadedTris)

        Application.getInstance().activityChanged.emit()

    def _onActiveStateChanged(self):
        controller = Application.getInstance().getController()
        active_tool = controller.getActiveTool()
        Logger.log("d", "Application.getInstance().getController().getActiveTool(): {}".format(active_tool))

        if active_tool == self:
            stage = controller.getActiveStage()
            controller.setFallbackTool(stage._our_toolset[0])
            if Selection.hasSelection():
                Selection.setFaceSelectMode(True)
                Logger.log("d", "Enabled faceSelectMode!")
            else:
                Selection.setFaceSelectMode(False)
                Logger.log("d", "Disabled faceSelectMode!")

            self._calculateMesh()

    ##  Get whether the select face feature is supported.
    #   \return True if it is supported, or False otherwise.
    def getSelectFaceSupported(self) -> bool:
        # Use a dummy postfix, since an equal version with a postfix is considered smaller normally.
        return Version(OpenGL.getInstance().getOpenGLVersion()) >= Version("4.1 dummy-postfix")

    def setSelectionMode(self, mode):
        Selection.clearFace()
        self._handle._connector.propertyHandler._selection_mode = mode
        Logger.log("d", "Changed selection mode to enum: {}".format(mode))
        #self._handle._connector.propertyHandler.selectedFacesChanged.emit()
        #self._onSelectedFaceChanged()

    def getSelectionMode(self):
        return self._handle._connector.propertyHandler._selection_mode

    def setAnchorSelection(self):
        self._handle.clearSelection()
        self.setSelectionMode(SelectionMode.AnchorMode)
        if self._handle._connector._proxy._anchorsApplied > 0:
            self._handle.drawSelection()

    def getAnchorSelectionActive(self):
        return self._handle._connector.propertyHandler._selection_mode is SelectionMode.AnchorMode

    def setLoadSelection(self):
        self._handle.clearSelection()
        self.setSelectionMode(SelectionMode.LoadMode)
        if self._handle._connector._proxy._loadsApplied > 0:
            self._handle.drawSelection()

    def getLoadSelectionActive(self):
        return self._handle._connector.propertyHandler._selection_mode is SelectionMode.LoadMode
