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
    WallOuterWipeDistance = 83
    WallTopSkinLayers = 84
    WallTopBottomThickness = 85
    WallTopThickness = 85
    WallTopLayers = 86
    WallBottomThickness = 87
    WallBottomLayers = 88
    WallTopBottomPattern = 89
    WallBottomInitialPattern = 90
    WallOuterInset = 91

    AlternateExtraWall = 95

    HorizontalExpansion = 110
  # Layers
    LayerHeight     =  100
    InitialLayerHeight = 101
    LineWidth       =  102
    WallLineWidth   =  103
    OuterLineWidth  =  104
    InnerLineWidth  =  105
    InfillLineWidth =  106
    InitialLayerLineWidth = 107
  # Skin & Orientation
    TopSkin         =  160
    BottomSkin      =  161
    TopOrientation  =  162
    BottomOrientation= 163
    SkinAngles      =  164

  # Material
    Material        =  170

  # Global Props
    GlobalProperty   = 1000
    ExtruderProperty = 1001
    

class SmartSliceLoadDirection(Enum):
    Pull = 1
    Push = 2

