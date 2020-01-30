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
from UM.Tool import Tool


#   Smart Slice Requirements Tool:
#     When Pressed, this tool produces the "Requirements Dialog"
#
class SmartSliceRequirements(Tool):
    #  Class Initialization
    def __init__(self):
        super().__init__()
