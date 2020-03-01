#   SmartSliceProperty.py
#   Teton Simulation
#   Authored on   December 11, 2019
#   Last Modified December 11, 2019

#
#   ENUMERATION of Properties involved with SmartSlice Validation/Optimization
#

#  Standard Imports
from enum import Enum

class SmartSliceProperty(Enum):
    # Mesh Properties
      MeshScale       =  1
      MeshRotation    =  2
      ModifierMesh    =  3
    # Requirements
      FactorOfSafety  =  11
      MaxDisplacement =  12
    # Loads/Anchors
      SelectedFace    =  20
      LoadMagnitude   =  21
      LoadDirection   =  22

    # Material
      Material        =  170

    # Global Props
      GlobalProperty   = 1000
      ExtruderProperty = 1001

class SmartSliceLoadDirection(Enum):
    Pull = 1
    Push = 2

'''
    Cura Property Keys that Explicitly affect SmartSlice results

    For list of settings that affect validation/optimization see:
        https://tetoncomposites.atlassian.net/wiki/spaces/CURA/pages/99549204/Validation+Workflow
        https://tetoncomposites.atlassian.net/wiki/spaces/CURA/pages/99549245/Optimization+Workflow

    For a list of strings that Cura correlates with settings see:
        https://github.com/Ultimaker/Cura/blob/master/resources/setting_visibility/expert.cfg
'''
class SmartSliceContainerProperties():
    def __init__(self):
        #  Global Settings
        self.global_keys = ["layer_height",                 #   Layer Height
                            "layer_height_0",               #   Initial Layer Height
                            "quality"]                      #   Quality Profile

        #  Per Extruder Settings
        self.extruder_keys = ["line_width",                 #  Line Width
                              "wall_line_width",            #  Wall Line Width
                              "wall_line_width_x",          #  Outer Wall Line Width
                              "wall_line_width_0",          #  Inner Wall Line Width
                              "wall_line_count",            #  Wall Line Count
                              "wall_thickness",             #  Wall Thickness
                              "skin_angles",                #  Skin (Top/Bottom) Angles
                              "top_layers",                 #  Top Layers
                              "bottom_layers",              #  Bottom Layers
                              "infill_pattern",             #  Infill Pattern
                              "infill_sparse_density",      #  Infill Density
                              "infill_angles",              #  Infill Angles
                              "infill_line_distance",       #  Infill Line Distance
                              "infill_sparse_thickness",    #  Infill Line Width
                              "alternate_extra_perimeter"]  #  Alternate Extra Walls

class SelectionMode:
    AnchorMode = 1
    LoadMode = 2

class SmartSlicePropertyColor():
    SubheaderColor = "#A9A9A9"
    WarningColor = "#F3BA1A"
    ErrorColor = "#F15F63"
    SuccessColor = "#5DBA47"

