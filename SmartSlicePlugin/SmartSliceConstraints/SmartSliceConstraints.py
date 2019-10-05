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


#  Ultimaker/Cura Imports
from UM.Scene.ToolHandle import ToolHandle
from UM.Mesh.MeshBuilder import MeshBuilder
from UM.Math.Vector import Vector


#
#   Smart Slice Constraints Tool:
#       When pressed, this tool produces the "Constraints Dialog", where the end-user can then
#       select a desired tool for applying boundary conditions, e.g. anchors/loads.
#
class SmartSliceConstraints(Tool):
  #  Class Initialization
  def __init__(self, parent = None):
    super().__init__(parent)
        
    #  Get CWD 
    base_path = PluginRegistry.getInstance().getPluginPath("SmartSliceConstraints")

    #  Constraints Tool Dialog
    component_path = os.path.join(base_path, "ui", "dialogConstraints.qml")
    self.addDisplayComponent("_constraints", component_path)


