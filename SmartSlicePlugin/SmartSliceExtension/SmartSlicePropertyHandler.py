#   SmartSlicePropertyHandler.py
#   Teton Simulation
#   Authored on   January 3, 2019
#   Last Modified January 3, 2019

#
#  Contains procedures for handling Cura Properties in accordance with SmartSlice
#

from .SmartSliceCloudProxy import SmartSliceCloudStatus
from .SmartSliceValidationProperty import SmartSliceValidationProperty

class SmartSlicePropertyHandler:
    def __init__(self, proxy):

        #  Callback
        self._proxy = proxy
        self.connector = self._proxy.connector
        
        #  Convenience
        self._activeExtruder = None
        self._activeMachineManager = None

        #  Cache Space
        self._changedFloat = None
        self._changedBool  = None
        self._changedString = None


        #  Shell
        self.alternateExtraWall = None
        self.skinAngles = None

        #  Walls
        self.wallThickness = None
        self.wallLineCount = None
        self.topThickness = None
        self.topLayers = None
        self.bottomLayers = None
        self.bottomThickness = None
        self.horizontalExpansion = None

        #  Line Widths / Layering
        self.layerHeight = None
        self.layerHeightInitial = None
        self.lineWidthInitialLayer = None
        self.lineWidth = None
        self.lineWidthWall = None
        self.lineWidthOuter = None
        self.lineWidthInner = None
        self.lineWidthTopBottom = None
        self.lineWidthInfill = None

        #  Infills
        self.infillDensity = None
        self.infillPattern = None
        self.infillLineDirection = None
        self.infillLineDistance = None
        self.infillAngles = None

    #  Second Stage Initialization
    def init(self):
        self._activeExtruder = self._proxy._activeExtruder
        self._activeMachineManager = self._proxy._activeMachineManager
        self._setInfillDefaults

        
    #
    #   QUALITY PROPERTIES
    #


    #
    #   SHELL PROPERTIES
    #

    #  Alternate Extra Wall (DISFUNCT)
    def setAlternateExtraWall(self):
        self._activeExtruder.setProperty("alternate_extra_wall", "value", self.alternateExtraWall)

    def onAlternateExtraWallChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._proxy._propertyChanged = SmartSliceValidationProperty.AlternateExtraWall
            self._changedBool = self._activeExtruder.getProperty("alternate_extra_wall", "value")
            self.connector._confirmValidation()
        else:
            self.alternateExtraWall = self._activeExtruder.getProperty("alternate_extra_wall", "value")

    #  Top/Bottom Line Directions (DISFUNCT)
    def setSkinAngles(self):
        self._activeExtruder.setProperty("skin_angles", "value", self.skinAngles)

    def onSkinAnglesChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._proxy._propertyChanged = SmartSliceValidationProperty.SkinAngles
            self._changedString = self._activeExtruder.getProperty("skin_angles", "value")
            self.connector._confirmValidation()
        else:
            self.skinAngles = self._activeExtruder.getProperty("skin_angles", "value")


    #
    #   INFILL PROPERTIES
    #

    #  Infill Line Distance
    def setInfillLineDistance(self):
        self._changedFloat = None
        self._activeExtruder.setProperty("infill_line_distance", "value", self.infillLineDistance)

    def onInfillLineDistanceChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._proxy._propertyChanged = SmartSliceValidationProperty.InfillLineDistance
            self._changedFloat = self._activeExtruder.getProperty("infill_line_distance", "value")
            self.connector._confirmValidation()
        else:
            self.infillLineDistance = self._activeExtruder.getProperty("infill_line_distance", "value")

    #  Infill Angles
    def setInfillAngles(self):
        self._changedString = None
        self._activeExtruder.setProperty("infill_angles", "value", self.infillAngles)

    def onInfillAnglesChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._proxy._propertyChanged = SmartSliceValidationProperty.InfillLineDistance
            self._changedFloat = self._activeExtruder.getProperty("infill_angles", "value")
            self.connector._confirmValidation()
        else:
            self.infillLineDistance = self._activeExtruder.getProperty("infill_angles", "value")

        #  Infills
    def _setInfillDefaults(self):
        self.infillPattern = self._activeExtruder.getProperty("infill_pattern", "value")

    def setInfillDensity(self):
        self._activeExtruder.setProperty("infill_sparse_density", "value", self.infillDensity)

    def onInfillDensityChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.InfillDensity
            self._changedValue = self._activeExtruder.getProperty("infill_sparse_density", "value")
            self.connector._confirmValidation()
        else:
            self.infillDensity = self._activeExtruder.getProperty("infill_sparse_density", "value")

    def setInfillPattern(self):
        self._activeExtruder.setProperty("infill_pattern", "value", self.infillPattern)

    def onInfillPatternChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.InfillPattern
            self._changedString = self._activeExtruder.getProperty("infill_pattern", "value")
            self.connector._confirmValidation()
        else:
            self.infillPattern = self._activeExtruder.getProperty("infill_pattern", "value")

    def setLayerHeight(self):
        self._changedFloat = None
        self._activeMachineManager._global_container_stack.setProperty("layer_height", "value", self.layerHeight)

    def onLayerHeightChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.LayerHeight
            self._changedFloat = self._activeMachineManager._global_container_stack.getProperty("layer_height", "value")
            self.connector._confirmValidation()
        else:
            self.layerHeight = self._activeMachineManager._global_container_stack.getProperty("layer_height", "value")

    def setInitialLayerHeight(self):
        self._changedFloat = None
        self._activeExtruder.setProperty("initial_layer_height", "value", self.layerHeightInitial)

    def onInitialLayerHeightChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.InitialLayerHeight
            self._changedFloat = self._activeExtruder.getProperty("initial_layer_height", "value")
            self.connector._confirmValidation()
        else:
            self.layerHeightInitial = self._activeExtruder.getProperty("initial_layer_height", "value")

    def onInitialLayerLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.InitialLayerLineWidth
            self._changedFloat = self._activeExtruder.getProperty("initial_layer_line_width", "value")
            self.connector._confirmValidation()
        else:
            self.lineWidthInitialLayer = self._activeExtruder.getProperty("initial_layer_line_width", "value")


    def setLineWidth(self):
        self._changedFloat = None
        self._activeExtruder.setProperty("line_width", "value", self.lineWidth)

    def onLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.LineWidth
            self._changedFloat = self._activeExtruder.getProperty("line_width", "value")
            self.connector._confirmValidation()
        else:
            self.lineWidth = self._activeExtruder.getProperty("line_width", "value")

    def setWallLineWidth(self):
        self._activeExtruder.setProperty("wall_line_width", "value", self.lineWidthWall)

    def onWallLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.WallLineWidth
            self._changedFloat = self._activeExtruder.getProperty("wall_line_width", "value")
            self.connector._confirmValidation()
        else:
            self.lineWidth = self._activeExtruder.getProperty("wall_line_width", "value")
        

    def setOuterLineWidth(self):
        self._activeExtruder.setProperty("outer_wall_line_width", "value", self.lineWidthOuter)

    def onOuterLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.OuterLineWidth
            self._changedFloat = self._activeExtruder.getProperty("outer_wall_line_width", "value")
            self.connector._confirmValidation()
        else:
            self.lineWidthOuter = self._activeExtruder.getProperty("outer_wall_line_width", "value")

    def setInnerLineWidth(self):
        self._activeExtruder.setProperty("inner_wall_line_width", "value", self.lineWidthInner)

    def onInnerLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.InnerLineWidth
            self._changedFloat = self._activeExtruder.getProperty("inner_wall_line_width", "value")
            self.connector._confirmValidation()
        else:
            self.lineWidthInner = self._activeExtruder.getProperty("inner_wall_line_width", "value")

    def setInfillLineWidth(self):
        self._activeExtruder.setProperty("infill_line_width", "value", self.lineWidthInfill)

    def onInfillLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.InfillLineWidth
            self._changedFloat = self._activeExtruder.getProperty("infill_line_width", "value")
            self.connector._confirmValidation()
        else:
            self.lineWidthInfill = self._activeExtruder.getProperty("infill_line_width", "value")




    def setWallThickness(self):
        self._activeExtruder.setProperty("wall_thickness", "value", self.wallThickness)

    def onWallThicknessChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.WallThickness
            self._changedValue = self._activeExtruder.getProperty("wall_thickness", "value")
            self.connector._confirmValidation()
        else:
            self.wallThickness = self._activeExtruder.getProperty("wall_thickness", "value")

    def setWallLineCount(self):
        self._activeExtruder.setProperty("wall_line_count", "value", self.wallLineCount)

    def onWallLineCountChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.WallLineCount
            self._changedValue = self._activeExtruder.getProperty("wall_line_count", "value")
            self.connector._confirmValidation()
        else:
            self.wallLineCount = self._activeExtruder.getProperty("wall_line_count", "value")


    #  Top Thickness
    def setTopThickness(self):
        self._activeExtruder.setProperty("top_thickness", "value", self.topThickness)

    def onTopThicknessChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.TopThickness
            self._changedValue = self._activeExtruder.getProperty("top_thickness", "value")
            self.connector._confirmValidation()
        else:
            self.topThickness = self._activeExtruder.getProperty("top_thickness", "value")

    #  Top Layers
    def setTopLayers(self):
        self._activeExtruder.setProperty("top_layers", "value", self.topLayers)

    def onTopLayersChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.TopLayers
            self._changedValue = self._activeExtruder.getProperty("top_layers", "value")
            self.connector._confirmValidation()
        else:
            self.topLayers = self._activeExtruder.getProperty("top_layers", "value")

    #  Bottom Thickness
    def setBottomThickness(self):
        self._activeExtruder.setProperty("bottom_thickness", "value",self.bottomThickness)

    def onBottomThicknessChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.BottomThickness
            self._changedValue = self._activeExtruder.getProperty("bottom_thickness", "value")
            self.connector._confirmValidation()
        else:
            self.bottomThickness = self._activeExtruder.getProperty("bottom_thickness", "value")
        
    #  Bottom Layers
    def setBottomLayers(self):
        self._activeExtruder.setProperty("bottom_layers", "value", self.bottomLayers)

    def onBottomLayersChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.BottomLayers
            self._changedValue = self._activeExtruder.getProperty("bottom_layers", "value")
            self.connector._confirmValidation()
        else:
            self.bottomLayers = self._activeExtruder.getProperty("bottom_layers", "value")

    #  Horizontal Expansion
    def setHorizontalExpansion(self):
        self._activeExtruder.setProperty("horizontal_expansion", "value", self.horizontalExpansion)

    def onHorizontalExpansionChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertyChanged = SmartSliceValidationProperty.HorizontalExpansion
            self._changedValue = self._activeExtruder.getProperty("horizontal_expansion", "value")
            self.connector._confirmValidation()
        else:
            self.horizontalExpansion = self._activeExtruder.getProperty("horizontal_expansion", "value")
    
    def onTopLineDirectionChanged(self):
        #  STUB 
        1 + 1

    def onBottomLineDirectionChanged(self):
        #  STUB 
        1 + 1

    def onMeshScaleChangd(self):
        #  STUB
        1 + 1

    def onMeshRotationChanged(self):
        #  STUB 
        1 + 1


