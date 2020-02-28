from typing import Any

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

from cura.CuraApplication import CuraApplication
from cura.Scene.CuraSceneNode import CuraSceneNode

#  QT / QML Imports
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtQml import QQmlComponent, QQmlContext # @UnresolvedImport

#  Local Imports
from ..utils import makeInteractiveMesh, findChildSceneNode
from ..stage import SmartSliceScene
from ..SmartSliceExtension import SmartSliceExtension
from ..SmartSliceProperty import SelectionMode

i18n_catalog = i18nCatalog("smartslice")

##  Provides the tool to rotate meshes and groups
#
#   The tool exposes a ToolHint to show the rotation angle of the current operation
class SmartSliceSelectTool(Tool):
    def __init__(self, extension : SmartSliceExtension):
        super().__init__()
        self.extension = extension

        self._connector = extension.cloud # SmartSliceCloudConnector
        self._mode = SelectionMode.AnchorMode

        #self._shortcut_key = Qt.Key_S

        self.setExposedProperties("AnchorSelectionActive",
                                  "LoadSelectionActive",
                                  "SelectionMode",
                                  )

        Selection.selectedFaceChanged.connect(self._onSelectedFaceChanged)

        #self._load_face = None
        self._bc_list = None

        self._controller.activeToolChanged.connect(self._onActiveStateChanged)

        self._connector._proxy.loadDirectionChanged.connect(self._onLoadDirectionChanged)
        self._connector._proxy.loadMagnitudeChanged.connect(self._onLoadMagnitudeChanged)

    ##  Handle mouse and keyboard events
    #
    #   \param event type(Event)
    def event(self, event):
        return super().event(event)

    def setActiveBoundaryConditionList(self, bc_list):
        self._bc_list = bc_list

    def _onSelectionChanged(self):
        super()._onSelectionChanged()

        # I think there should be a better way, but this is in place
        # to force a full render when the selection changes. Without
        # this a different event is required (e.g. a camera rotate) to
        # get a render update after clicking on or off the shown scene node.
        # This behavior is probably indicative of something we're doing
        # wrong - we might need to dive into this at some point
        window = CuraApplication.getInstance().getMainWindow()
        if window:
            window._full_render_required = True
            window.update()

    def _onSelectedFaceChanged(self, curr_sf=None):
        if not self.getEnabled():
            return

        curr_sf = Selection.getSelectedFace()
        if curr_sf is None:
            return

        node, face_id = curr_sf

        smart_slice_node = findChildSceneNode(node, SmartSliceScene.Root)

        if self._bc_list is None:
            return

        bc_node = self._bc_list.getActiveNode()

        if bc_node is None:
            return

        tris = list(smart_slice_node.getInteractiveMesh().select_planar_face(face_id))

        bc_node.setMeshDataFromPywimTriangles(tris)

        self._connector.propertyHandler.selectedFaceChanged(tris, self._mode)

    def _onLoadDirectionChanged(self):
        raise Exception('Shouldn\'t be hitting this function any more - TODO remove')
        if isinstance(bc_node, SmartSliceScene.LoadFace):
            bc_node.setArrowDirection(self._connector._proxy.loadDirection)

    def _onLoadMagnitudeChanged(self):
        raise Exception('Shouldn\'t be hitting this function any more - TODO remove')
        if isinstance(bc_node, SmartSliceScene.LoadFace):
            bc_node.force.magnitude = self._connector._proxy.loadMagnitude

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

    ##  Get whether the select face feature is supported.
    #   \return True if it is supported, or False otherwise.
    def getSelectFaceSupported(self) -> bool:
        # Use a dummy postfix, since an equal version with a postfix is considered smaller normally.
        return Version(OpenGL.getInstance().getOpenGLVersion()) >= Version("4.1 dummy-postfix")

    def setSelectionMode(self, mode):
        Selection.clearFace()
        self._mode = mode
        Logger.log("d", "Changed selection mode to: {}".format(mode))

    def setAnchorSelection(self):
        self.setSelectionMode(SelectionMode.AnchorMode)

    def setLoadSelection(self):
        self.setSelectionMode(SelectionMode.LoadMode)

    def getSelectionMode(self):
        return self._mode

    def getAnchorSelectionActive(self):
        return self._mode == SelectionMode.AnchorMode

    def getLoadSelectionActive(self):
        return self._mode == SelectionMode.LoadMode
