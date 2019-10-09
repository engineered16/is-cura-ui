#   SmartSliceRequirements.py
#   Teton Simulation
#   Authored on   October 8, 2019
#   Last Modified October 8, 2019

#
#   Contains definitions for the "Requirements" Tool, which serves as an interface for requirements
#
#   Types of Requirements:
#     * Safety Factor
#     * Maximum Deflection
#

#   Filesystem Control
import os.path

#   Ultimaker/Cura Imports
from UM.Application import Application
from UM.Tool import Tool
from UM.Scene.ToolHandle import ToolHandle
from UM.Mesh.MeshBuilder import MeshBuilder     #  Deprecated
from UM.PluginRegistry import PluginRegistry
from UM.Math.Vector import Vector           #  Deprecated


#   Smart Slice Requirements Tool:
#     When Pressed, this tool produces the "Requirements Dialog"
#
class SmartSliceRequirements(Tool):
    #  Class Initialization
    def __init__(self):
        super().__init__()

        #   Connect Stage to Cura Application
        Application.getInstance().engineCreatedSignal.connect(self._engineCreated)

    def _engineCreated(self):
        """
        Executed when the Qt/QML engine is up and running.
        This is at the time when all plugins are loaded, slots registered and basic signals connected.
        """

        #  Get CWD
        base_path = PluginRegistry.getInstance().getPluginPath("SmartSliceRequirements")

        #  Constraints Tool Dialog
        component_path = os.path.join(base_path, "ui", "dialogRequirements.qml")
        # We are a Tool here and no Stage or something similar..
        # The following line won't work.
        #self.addDisplayComponent("_requirements", component_path)
