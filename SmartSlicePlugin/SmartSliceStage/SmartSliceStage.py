#######################################
#   SmartSliceStage.py
#   Teton Simulation, Inc; Ultimaker
#   Last Modified October 17, 2019
#######################################

#
#   Contains backend-interface for Smart Slice Stage
#
#   A STAGE is the component within Cura that contains all other
#   related major features.  This provides a vehicle to transition
#   between Smart Slice and other major Cura stages (e.g. 'Prepare')
#
#   SmartSliceStage is responsible for transitioning into the Smart
#   Slice user environment. This enables SmartSlice features, such as
#   setting anchors/loads and requesting AWS jobs.
#


#   Filesystem Control
import os.path

#   Expose Ultimaker/Cura API
from UM.Logger import Logger
from UM.Application import Application
from UM.PluginRegistry import PluginRegistry
from UM.Scene.Selection import Selection

from cura.Stages.CuraStage import CuraStage

from .ui.Bridge import SmartSliceBridge
from PyQt5.QtQml import QQmlComponent, QQmlContext # @UnresolvedImport

#
#   Stage Class Definition
#
class SmartSliceStage(CuraStage):
    def __init__(self, parent=None):
        super().__init__(parent)

        #   Connect Stage to Cura Application
        Application.getInstance().engineCreatedSignal.connect(self._engineCreated)

        #   Set Default Attributes
        self._was_buildvolume_hidden = None
        self._default_toolset = None
        self._default_fallback_tool = None
        self._our_toolset = ("SmartSliceSelectTool",
                             "SmartSliceRequirements",
                             )
        #self._tool_blacklist = ("SelectionTool", "CameraTool")
        self._our_last_tool = None
        self._were_tools_enabled = None
        self._was_selection_face = None

    #   onStageSelected:
    #       This transitions the userspace/working environment from
    #       current stage into the Smart Slice User Environment.
    def onStageSelected(self):
        buildvolume = Application.getInstance().getBuildVolume()
        if buildvolume.isVisible():
            buildvolume.setVisible(False)
            self._was_buildvolume_hidden = True

        # Ensure we have tools defined and apply them here
        self.setToolVisibility(True)
        Application.getInstance().getController().setFallbackTool(self._our_toolset[0])
        Application.getInstance().getController().setActiveTool(None)

    #   onStageDeselected:
    #       Sets attributes that allow the Smart Slice Stage to properly deactivate
    #       This occurs before the next Cura Stage is activated
    def onStageDeselected(self):
        if self._was_buildvolume_hidden:
            buildvolume = Application.getInstance().getBuildVolume()
            buildvolume.setVisible(True)
            self._is_buildvolume_hidden = None

        # Recover if we have tools defined
        self.setToolVisibility(False)
        Application.getInstance().getController().setFallbackTool(self._default_fallback_tool)
        Application.getInstance().getController().setActiveTool(None)

        # Reset selection
        if self._was_selection_face is not None and self._was_selection_face is not Selection.getFaceSelectMode():
            Selection.setFaceSelectMode(self._was_selection_face)
        Selection.clear()
        Selection.clearFace()

    def getVisibleTools(self):
        visible_tools = []
        tools = Application.getInstance().getController().getAllTools().keys()
        for tool in tools:
            visible = True
            tool_metainfo = PluginRegistry.getInstance().getMetaData(tool).get("tool", {})
            keys = tool_metainfo.keys()
            if "visible" in keys:
                visible = tool_metainfo["visible"]

            if visible:
                visible_tools.append(tool)
        return visible_tools

    def setToolVisibility(self, our_tools_visible):
        plugin_registry = PluginRegistry.getInstance()
        for tool_id in Application.getInstance().getController().getAllTools().keys():
            tool_metadata = plugin_registry.getMetaData(tool_id)
            if tool_id in self._our_toolset:
                tool_metadata.get("tool", {})["visible"] = our_tools_visible
            elif tool_id in self._default_toolset:
                tool_metadata.get("tool", {})["visible"] = not our_tools_visible

            if "visible" in tool_metadata.get("tool", {}).keys():
                state = tool_metadata.get("tool", {})["visible"]
                Logger.log("d", "Visibility of <{}>: {}".format(tool_id, state))

        Application.getInstance().getController().toolsChanged.emit()

    @property
    def our_toolset(self):
        """
        Generates a dictionary of tool id and instance from our id list in __init__.
        """
        our_toolset_with_objects = {}
        for tool in self._our_toolset:
            our_toolset_with_objects[tool] = PluginRegistry.getInstance().getPluginObject(tool)
        return our_toolset_with_objects

    @property
    def our_first_tool(self):
        """
        Takes the first tool if out of our tool dictionary.
        Defining a dict here is the way Cura's controller works.
        """
        return list(self.our_toolset.keys())[0]

    def _engineCreated(self):
        """
        Executed when the Qt/QML engine is up and running.
        This is at the time when all plugins are loaded, slots registered and basic signals connected.
        """

        base_path = PluginRegistry.getInstance().getPluginPath("SmartSliceStage")

        # Slicing windows in lower right corner
        component_path = os.path.join(base_path, "ui", "SmartSliceMain.qml")
        self.addDisplayComponent("main", component_path)

        # Top menu bar of stage
        component_path = os.path.join(base_path, "ui", "SmartSliceMenu.qml")
        self.addDisplayComponent("menu", component_path)

        # Setting state after all plugins are loaded
        self._was_buildvolume_hidden = not Application.getInstance().getBuildVolume().isVisible()

        # Get all visible tools and exclude our tools from the list
        self._default_toolset = self.getVisibleTools()
        for tool in self._default_toolset:
            if tool in self._our_toolset:
                self._default_toolset.remove(tool)
                
        self._default_fallback_tool = Application.getInstance().getController().getFallbackTool()

        # Undisplay our tools!
        self.setToolVisibility(False)
