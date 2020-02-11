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
    Cura Property Keys that explicitly affect SmartSlice results
    For list of settings that affect validation/optimization see:
        https://tetoncomposites.atlassian.net/wiki/spaces/CURA/pages/99549204/Validation+Workflow
        https://tetoncomposites.atlassian.net/wiki/spaces/CURA/pages/99549245/Optimization+Workflow
'''
class SmartSliceContainerProperties():
    def __init__(self):
        #  Global Settings
        self.global_keys = {"layer_height",     #   Layer Height 
                            "layer_height_0"}   #   Initial Layer Height

        #  Per Extruder Settings
        self.extruder_keys = {"line_width",             #  Line Width 
                              "wall_line_width",        #  Wall Line Width
                              "wall_line_width_x",      #  Outer Wall Line Width
                              "wall_line_width_0",      #  Inner Wall Line Width
                              "wall_line_count",        #  Wall Line Count
                              "wall_thickness",         #  Wall Thickness
                              "skin_angles",            #  Skin (Top/Bottom) Angles
                              "top_layers",             #  Top Layers
                              "bottom_layers",          #  Bottom Layers
                              "infill_pattern",         #  Infill Pattern
                              "infill_sparse_density",  #  Infill Density
                              "infill_angles",          #  Infill Angles
                              "alternate_extra_perimeter"}  #  Alternate Extra Walls