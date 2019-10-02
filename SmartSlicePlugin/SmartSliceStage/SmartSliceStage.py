import os.path

from UM.Logger import Logger
from UM.Application import Application
from UM.PluginRegistry import PluginRegistry
from UM.Scene.Selection import Selection

from cura.Stages.CuraStage import CuraStage


class SmartSliceStage(CuraStage):
    def __init__(self, parent=None):
        super().__init__(parent)

        Application.getInstance().engineCreatedSignal.connect(self._engineCreated)

        self._stage_open = False
        self._was_buildvolume_hidden = None
        self._default_tool_set = None
        self._our_toolset = ["SmartSliceSelectTool",
                             ]
        self._our_last_tool = None
        self._were_tools_enabled = None
        self._was_selection_face = None

    def onStageSelected(self):
        buildvolume = Application.getInstance().getBuildVolume()
        if buildvolume.isVisible():
            buildvolume.setVisible(False)
            self._was_buildvolume_hidden = True
        
        # Ensure we have tools defined and apply them here
        if self._our_toolset:
            # Tool: Making a snapshot...
            if not self._default_tool_set:
                self._default_tool_set = Application.getInstance().getController()._tools
            self._was_active_tool = Application.getInstance().getController().getActiveTool()
            self._were_tools_enabled = Application.getInstance().getController().getToolsEnabled()
            
            # Tool: Replacing toolset
            Application.getInstance().getController()._tools = self.our_toolset
            
            # Tool: Active state
            if not self._our_last_tool:
                self._our_last_tool = self.our_first_tool
            Application.getInstance().getController().setActiveTool(self._our_last_tool)

            # Tool: Enabled state
            #Application.getInstance().getController().setToolsEnabled(False)
            
            # Tool: Emitting signal to announce our changes
            Application.getInstance().getController().toolsChanged.emit()

        # Reset selection
        self._was_selection_face = Selection.getFaceSelectMode()
        Selection.setFaceSelectMode(False)
        Selection.clear()
        Selection.clearFace()


    def onStageDeselected(self):
        if self._was_buildvolume_hidden:
            buildvolume = Application.getInstance().getBuildVolume()
            buildvolume.setVisible(True)
            self._is_buildvolume_hidden = None
        
        # Recover if we have tools defined
        if self._our_toolset:
            Application.getInstance().getController()._tools = self._default_tool_set
            Application.getInstance().getController().toolsChanged.emit()
        
            # Tool: Active state
            Application.getInstance().getController().setActiveTool(self._was_active_tool)

            # Tool: Enabled state
            if self._were_tools_enabled is not None:
                if self._were_tools_enabled is not Application.getInstance().getController().getToolsEnabled():
                    Application.getInstance().getController().setToolsEnabled(self._were_tools_enabled)

        if self._was_selection_face is not None and self._was_selection_face is not Selection.getFaceSelectMode():
            Selection.setFaceSelectMode(self._was_selection_face)

        # Reset selection
        if self._was_selection_face is not None and self._was_selection_face is not Selection.getFaceSelectMode():
            Selection.setFaceSelectMode(self._was_selection_face)
        Selection.clear()
        Selection.clearFace()

    @property
    def our_toolset(self):
        plugin_registry = Application.getInstance()._plugin_registry
        our_toolset_with_objects = {}
        for tool in self._our_toolset:
            our_toolset_with_objects[tool] = plugin_registry.getPluginObject(tool)
        return our_toolset_with_objects

    @property
    def our_first_tool(self):
        return list(self.our_toolset.keys())[0]

    def _engineCreated(self):
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
        for tool in self._our_toolset:
            if tool in Application.getInstance().getController()._tools.keys():
                Logger.log("d", "Removing <{}> tool from the default toolset!".format(tool))
                del Application.getInstance().getController()._tools[tool]
                tool_removed = True
        if tool_removed:
            Application.getInstance().getController().toolsChanged.emit()
        
