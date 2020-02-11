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

