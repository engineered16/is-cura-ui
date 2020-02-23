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

import os.path


#   Expose Ultimaker/Cura API
from UM.Logger import Logger
from UM.Application import Application
from UM.PluginRegistry import PluginRegistry

from cura.Stages.CuraStage import CuraStage
from cura.CuraApplication import CuraApplication

#
#   Stage Class Definition
#
class SmartSliceStage(CuraStage):
    def __init__(self, extension, parent=None):
        super().__init__(parent)

        #   Connect Stage to Cura Application
        Application.getInstance().engineCreatedSignal.connect(self._engineCreated)
        self._connector = extension

        #   Set Default Attributes
        self._was_buildvolume_hidden = None
        self._was_overhang_visible = None
        self._overhang_visible_preference = "view/show_overhang"
        self._default_toolset = None
        self._default_fallback_tool = None
        self._our_toolset = ("SmartSlicePlugin_SelectTool",
                             "SmartSlicePlugin_RequirementsTool",
                             )
        #self._tool_blacklist = ("SelectionTool", "CameraTool")
        self._our_last_tool = None
        self._were_tools_enabled = None
        self._was_selection_face = None
        self._previous_tool = None

    #   onStageSelected:
    #       This transitions the userspace/working environment from
    #       current stage into the Smart Slice User Environment.
    def onStageSelected(self):
        application = Application.getInstance()
        
        buildvolume = application.getBuildVolume()
        if buildvolume.isVisible():
            buildvolume.setVisible(False)
            self._was_buildvolume_hidden = True
            
        # Overhang visiualization
        self._was_overhang_visible = application.getPreferences().getValue(self._overhang_visible_preference)
        application.getPreferences().setValue(self._overhang_visible_preference, False)

        if self._previous_tool:
            application.getController().setActiveTool(self._previous_tool)
        else:
            # Ensure we have tools defined and apply them here
            use_tool = self._our_toolset[0]
            application.getController().setFallbackTool(use_tool)
            self._previous_tool = application.getController().getActiveTool()
            
        self.setToolVisibility(True)

        #  Set the Active Extruder for the Cloud interactions
        self._connector._proxy._activeMachineManager = CuraApplication.getInstance().getMachineManager()
        self._connector._proxy._activeExtruder = self._connector._proxy._activeMachineManager._global_container_stack.extruderList[0]

        if not self._connector.propertyHandler._initialized:
            self._connector.propertyHandler.cacheChanges()
            self._connector.propertyHandler._initialized = True
        
    #   onStageDeselected:
    #       Sets attributes that allow the Smart Slice Stage to properly deactivate
    #       This occurs before the next Cura Stage is activated
    def onStageDeselected(self):
        application = Application.getInstance()
        
        if self._was_buildvolume_hidden:
            buildvolume = application.getBuildVolume()
            buildvolume.setVisible(True)
            self._is_buildvolume_hidden = None

        if self._was_overhang_visible is not None:
            application.getPreferences().setValue(self._overhang_visible_preference,
                                                  self._was_overhang_visible)

        # Recover if we have tools defined
        self.setToolVisibility(False)
        application.getController().setFallbackTool(self._default_fallback_tool)
        if self._previous_tool:
            application.getController().setActiveTool(self._default_fallback_tool)

        #  Hide all visible SmartSlice UI Components

        

    def getVisibleTools(self):
        visible_tools = []
        tools = Application.getInstance().getController().getAllTools()
        """
        plugin_registry = PluginRegistry.getInstance()
        for tool in tools:
            visible = True
            tool_metainfos = plugin_registry.getMetaData(tool).get("tool", {})
            if type(tool_metainfos) is dict:
                tool_metainfos = [tool_metainfos]
            for tool_metainfo in tool_metainfos:
                keys = tool_metainfo.keys()
                if "visible" in keys:
                    visible = tool_metainfo["visible"]
    
                if visible and tool not in visible_tools:
                    visible_tools.append(tool)
        """
        for name in tools:
            visible = True
            tool_metainfo = tools[name].getMetaData()

            if "visible" in tool_metainfo.keys():
                visible = tool_metainfo["visible"]

            if visible:
                visible_tools.append(name)
            
            Logger.log("d", "Visibility of <{}>: {}".format(name,
                                                            visible,
                                                            )
            )

        return visible_tools

    # Function to make our tools either visible or not and the other tools the opposite
    def setToolVisibility(self, our_tools_visible):
        """
        plugin_registry = PluginRegistry.getInstance()
        for tool_id in Application.getInstance().getController().getAllTools().keys():
            plugin_metadata = plugin_registry.getMetaData(tool_id)
            tool_metadatas = plugin_metadata.get("tool", {})
            if type(tool_metadatas) is dict:
                tool_metadatas = [tool_metadatas]
            for tool_metadata in tool_metadatas:
                if tool_id in self._our_toolset:
                    tool_metadata["visible"] = our_tools_visible
                elif tool_id in self._default_toolset:
                    tool_metadata["visible"] = not our_tools_visible
                
                Logger.log("d", "Visibility of <{}>: {}".format(plugin_metadata["id"],
                                                                tool_metadata["visible"],
                                                                )
                )
        """
        tools = Application.getInstance().getController().getAllTools()
        for name in tools:
            tool_meta_data = tools[name].getMetaData()
            
            if name in self._our_toolset:
                tool_meta_data["visible"] = our_tools_visible
            elif name in self._default_toolset:
                tool_meta_data["visible"] = not our_tools_visible
            
            Logger.log("d", "Visibility of <{}>: {}".format(name,
                                                            tool_meta_data["visible"],
                                                            )
            )

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

        base_path = PluginRegistry.getInstance().getPluginPath("SmartSlicePlugin")

        # Slicing windows in lower right corner
        component_path = os.path.join(base_path, "stage", "ui", "SmartSliceMain.qml")
        self.addDisplayComponent("main", component_path)

        # Top menu bar of stage
        component_path = os.path.join(base_path, "stage", "ui", "SmartSliceMenu.qml")
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
