#   SmartSliceValidationProperty.py
#   Teton Simulation
#   Authored on   December 11, 2019
#   Last Modified December 11, 2019

#
#   ENUMERATION of Properties involved with SmartSlice Validation
#

#  Standard Imports
from enum import Enum

class SmartSliceValidationProperty(Enum):
  # Requirements
    FactorOfSafety  =  11
    MaxDisplacement =  12
  # Loads/Anchors
    SelectedFace    =  20
    LoadMagnitude   =  21
    LoadDirection   =  22
  # Infill Properties
    InfillDensity   =  40
    InfillPattern   =  41
    InfillOrientation= 42
  # Walls
    WallsCount      =  50
  # Skin & Orientation
    TopSkin         =  60
    BottomSkin      =  61
    TopOrientation  =  62
    BottomOrientation= 63
  # Layers
    LayerHeight     =  70
    LayerWidth      =  71

  # Material
    Material        =  80
    

class SmartSliceLoadDirection(Enum):
    Push = 1
    Pull = 2

