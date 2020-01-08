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
    InfillLineDistance = 42
    InfillAngles    = 43
    InfillLineMultiplier = 44
    InfillOffsetX   = 45
    InfillOffsetY   = 46
    InfillOverlapPer = 47
    InfillOverlapMM  = 48
    InfillWipeDistance = 49
    InfillLayerThickness = 50
    InfillGradualSteps = 51
    InfillBeforeWalls = 52
    InfillMinimumArea = 53
    InfillSupport     = 54
  # Skins
    SkinRemovalWidth = 55
    SkinTopRemovalWidth = 56
    SkinBottomRemovalWidth = 57
    SkinExpandDistance = 58
    SkinTopExpandDistance = 59
    SkinBottomExpandDistance = 60
    SkinMaxAngleExpansion = 61
    SkinMinWidthExpansion = 62
  # Walls
    WallsCount      =  80
    WallThickness   =  81
    WallLineCount   =  82
    AlternateExtraWall = 83
  # Skin & Orientation
    TopSkin         =  60
    BottomSkin      =  61
    TopOrientation  =  62
    BottomOrientation= 63
    SkinAngles      =  64
  # Layers
    LayerHeight     =  100
    InitialLayerHeight = 101
    LineWidth       =  102
    WallLineWidth   =  103
    OuterLineWidth  =  104
    InnerLineWidth  =  105
    InfillLineWidth =  106
    InitialLayerLineWidth = 107

    LayerWidth      =  111
    HorizontalExpansion = 112
    TopThickness    =  120
    TopLayers       =  121
    BottomThickness =  122
    BottomLayers    =  123

  # Material
    Material        =  150
    

class SmartSliceLoadDirection(Enum):
    Push = 1
    Pull = 2

