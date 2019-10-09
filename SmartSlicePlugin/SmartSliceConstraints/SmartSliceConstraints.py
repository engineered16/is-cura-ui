#   SmartSliceConstraints.py
#   Teton Simulation
#   Authored on   October 5, 2019
#   Last Modified October 5, 2019

#
#   Contains definition for the "Constraints" Tool, which serves as an interface for Smart Slice boundary conditions.
#
#   Types of Boundary Conditions:
#     * Loads
#     * Anchors
#

#   Filesystem Control
import os.path

#  Ultimaker/Cura Imports
from UM.Application import Application
from UM.Scene.ToolHandle import ToolHandle
from UM.Mesh.MeshBuilder import MeshBuilder
from UM.Math.Vector import Vector
from UM.PluginRegistry import PluginRegistry
from UM.Tool import Tool


#
#   Smart Slice Constraints Tool:
#       When pressed, this tool produces the "Constraints Dialog", where the end-user can then
#       select a desired tool for applying boundary conditions, e.g. anchors/loads.
#
class SmartSliceConstraints(Tool):
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
        base_path = PluginRegistry.getInstance().getPluginPath("SmartSliceConstraints")

        #  Constraints Tool Dialog
        component_path = os.path.join(base_path, "ui", "dialogConstraints.qml")
        # We are a Tool here and no Stage or something similar..
        # The following line won't work.
        #self.addDisplayComponent("_constraints", component_path)
