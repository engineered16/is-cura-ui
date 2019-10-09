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

#   Ultimaker/Cura Imports
from UM.scene.ToolHandle import ToolHandle
from UM.Mesh.Builder import MeshBuilder     #  Deprecated
from UM.Math.Vector import Vector           #  Deprecated



#
#   Smart Slice Requirements Tool: 
#     When Pressed, this tool produces the "Requirements Dialog"
#
class SmartSliceRequirements(Tool):
  #  Class Initialization
  def __init__(self, parent = None):
    super().__init__(parent)
        
    #  Get CWD 
    base_path = PluginRegistry.getInstance().getPluginPath("SmartSliceRequirements")

    #  Requirements Tool Dialog
    component_path = os.path.join(base_path, "ui", "dialogRequirements.qml")
    self.addDisplayComponent("_requirements", component_path)




