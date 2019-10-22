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
        self._stage_open = False
        self._was_buildvolume_hidden = None
        self._default_tool_set = None
        self._our_toolset = ["SmartSliceSelectTool",
                             "SmartSliceRequirements",
                             ]
        self._tool_blacklist = ("SelectionTool", "CameraTool")
        self._our_last_tool = None
        self._were_tools_enabled = None
        self._was_selection_face = None
        self._first_open = True

    #   onStageSelected:
    #       This transitions the userspace/working environment from
    #       current stage into the Smart Slice User Environment.
    def onStageSelected(self):
        buildvolume = Application.getInstance().getBuildVolume()
        if buildvolume.isVisible():
            buildvolume.setVisible(False)
            self._was_buildvolume_hidden = True

        # Ensure we have tools defined and apply them here
        for tool_id in Application.getInstance().getController().getAllTools().keys():
            if tool_id not in self._tool_blacklist:
                visible = tool_id in self._our_toolset
                PluginRegistry.getInstance().getMetaData(tool_id).get("tool", {})["visible"] = visible
                Logger.log("d", "Setting tool <{}> visible = {}".format(tool_id, visible))
                Application.getInstance().getController().toolsChanged.emit()

        # Reset selection
        self._was_selection_face = Selection.getFaceSelectMode()
        Selection.setFaceSelectMode(False)
        Selection.clear()
        Selection.clearFace()


        if (self._first_open):
            #  Create QML/Python Interface Bridge
            bridge = SmartSliceBridge()
            self._first_open = False


    #   onStageDeselected:
    #       Sets attributes that allow the Smart Slice Stage to properly deactivate
    #       This occurs before the next Cura Stage is activated
    def onStageDeselected(self):
        if self._was_buildvolume_hidden:
            buildvolume = Application.getInstance().getBuildVolume()
            buildvolume.setVisible(True)
            self._is_buildvolume_hidden = None

        # Recover if we have tools defined
        for tool_id in Application.getInstance().getController().getAllTools().keys():
            if tool_id not in self._tool_blacklist:
                visible = not tool_id in self._our_toolset
                PluginRegistry.getInstance().getMetaData(tool_id).get("tool", {})["visible"] = visible
                Logger.log("d", "Setting tool <{}> visible = {}".format(tool_id, visible))
                Application.getInstance().getController().toolsChanged.emit()

        if self._was_selection_face is not None and self._was_selection_face is not Selection.getFaceSelectMode():
            Selection.setFaceSelectMode(self._was_selection_face)

        # Reset selection
        if self._was_selection_face is not None and self._was_selection_face is not Selection.getFaceSelectMode():
            Selection.setFaceSelectMode(self._was_selection_face)
        Selection.clear()
        Selection.clearFace()

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

        # Remove our tools from the default toolset
        tool_removed = False
        tools_loaded = Application.getInstance().getController()._tools.keys()
        Logger.log("d", "The following tools are currently registered: {}".format(tools_loaded))
        for tool in self._our_toolset:
            if tool in Application.getInstance().getController()._tools.keys():
                Logger.log("d", "Removing <{}> tool from the default toolset!".format(tool))
                #tool_object = Application.getInstance().getController().getAllTools()[tool]
                #print(tool_object.getExposedProperties())
                #print(dir(tool_object.getExposedProperties()))
                #tool_object._enabled = False
                #tool_object._onToolEnabledChanged.emit()
                PluginRegistry.getInstance().getMetaData(tool).get("tool", {})["visible"] = False
                #del Application.getInstance().getController()._tools[tool]
                tool_removed = True
        if tool_removed:
            Application.getInstance().getController().toolsChanged.emit()
