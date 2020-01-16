#   SmartSlicePropertyHandler.py
#   Teton Simulation
#   Authored on   January 3, 2019
#   Last Modified January 3, 2019

#
#  Contains procedures for handling Cura Properties in accordance with SmartSlice
#

import copy
from copy import copy

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import QObject

#  Cura
from UM.Application import Application
from UM.Scene.Selection import Selection
from cura.CuraApplication import CuraApplication


#  Smart Slice
from .SmartSliceCloudProxy import SmartSliceCloudStatus
from .SmartSliceValidationProperty import SmartSliceValidationProperty

class SmartSlicePropertyHandler(QObject):
    def __init__(self, connector):
        super().__init__()

        #  Callback
        self.connector = connector
        self._confirming = False
        
        self._activeMachineManager = CuraApplication.getInstance().getMachineManager()
        self._activeExtruder = self._activeMachineManager._global_container_stack.extruderList[0]
        global_stack = Application.getInstance().getGlobalContainerStack()
        
        #  Cache Space
        self._propertiesChanged = []
        self._changedValues     = []

        #
        #   DEFAULT PROPERTY VALUES
        #

        #  Shell
        self.wallThickness = self._activeExtruder.getProperty("wall_thickness", "value")
        self.wallLineCount = self._activeExtruder.getProperty("wall_line_count", "value")
        self.wallOuterWipeDist = self._activeExtruder.getProperty("wall_0_wipe_dist", "value")
        self.wallRoofingLayers = self._activeExtruder.getProperty("roofing_layer_count", "value")
        self.wallTopBottomThick = self._activeExtruder.getProperty("top_bottom_thickness", "value")
        self.wallTopThickness = self._activeExtruder.getProperty("top_thickness", "value")
        self.wallTopLayers = self._activeExtruder.getProperty("top_layers", "value")
        self.wallBottomThickness = self._activeExtruder.getProperty("bottom_thickness", "value")
        self.wallBottomLayers = self._activeExtruder.getProperty("bottom_layers", "value")
        self.wallTopBottomPattern = self._activeExtruder.getProperty("top_bottom_pattern", "value")
        self.wallBottomInitialPattern = self._activeExtruder.getProperty("top_bottom_pattern_0", "value")
        self.wallSkinAngles = self._activeExtruder.getProperty("skin_angles", "value")
        self.wallOuterInset = self._activeExtruder.getProperty("wall_0_inset", "value")

        #  Line Widths / Layering
        self.layerHeight = self._activeExtruder.getProperty("layer_height", "value")
        self.layerHeightInitial = self._activeExtruder.getProperty("layer_height_0", "value")
        self.lineWidth = self._activeExtruder.getProperty("line_width", "value")
        self.lineWidthInitialLayer = self._activeExtruder.getProperty("line_width_0", "value")
        self.lineWidthWall = self._activeExtruder.getProperty("wall_line_width", "value")
        self.lineWidthOuter = self._activeExtruder.getProperty("wall_line_width_0", "value")
        self.lineWidthInner = self._activeExtruder.getProperty("wall_line_width_x", "value")
        self.lineWidthTopBottom = None
        self.lineWidthInfill = self._activeExtruder.getProperty("infill_line_width", "value")

        #  Infills
        self.infillDensity = self._activeExtruder.getProperty("infill_sparse_density", "value")
        self.infillLineDistance = self._activeExtruder.getProperty("infill_line_distance", "value")
        self.infillPattern = self._activeExtruder.getProperty("infill_pattern", "value")
        self.infillLineDirection = self._activeExtruder.getProperty("infill_angles", "value")
        self.infillOffsetX = self._activeExtruder.getProperty("infill_offset_x", "value")
        self.infillOffsetY = self._activeExtruder.getProperty("infill_offset_y", "value")
        self.infillMultiplier = self._activeExtruder.getProperty("infill_multiplier", "value")
        self.infillOverlapPercentage = self._activeExtruder.getProperty("infill_overlap_percentage", "value")
        self.infillOverlapMM = self._activeExtruder.getProperty("infill_overlap_mm", "value")
        self.infillWipeDist = self._activeExtruder.getProperty("infill_wipe_dist", "value")
        self.infillLayerThick = self._activeExtruder.getProperty("infill_layer_thickness", "value")
        self.infillGradSteps = self._activeExtruder.getProperty("gradual_infill_steps", "value")
        self.infillBeforeWalls = self._activeExtruder.getProperty("infill_before_walls", "value")
        self.infillMinimumArea = self._activeExtruder.getProperty("min_infill_area", "value")
        self.infillSupport = self._activeExtruder.getProperty("infill_support_enabled", "value")

        #  Skins
        self.skinRemovalWidth = self._activeExtruder.getProperty("skin_preshrink", "value")
        self.skinRemovalTop = self._activeExtruder.getProperty("top_skin_preshrink", "value")
        self.skinRemovalBottom = self._activeExtruder.getProperty("bottom_skin_preshrink", "value")
        self.skinExpandDistance = self._activeExtruder.getProperty("expand_skins_expand_distance", "value")
        self.skinExpandTop = self._activeExtruder.getProperty("top_skin_expand_distance", "value")
        self.skinExpandBottom = self._activeExtruder.getProperty("bottom_skin_expand_distance", "value")
        self.skinExpandMaxAngle = self._activeExtruder.getProperty("max_skin_angle_for_expansion", "value")
        self.skinExpandMinWidth = self._activeExtruder.getProperty("min_skin_width_for_expansion", "value")


        #  Mesh Properties
        self.meshScale    = None
        self.meshRotation = None
        self._sceneNode = None
        self._sceneRoot = Application.getInstance().getController().getScene().getRoot()

        self._material = self._activeMachineManager._global_container_stack.extruderList[0].material #  Cura Material Node
        
        #  Connect Signals
        global_stack.propertyChanged.connect(self._onGlobalPropertyChanged)
        self._activeExtruder.propertyChanged.connect(self._onExtruderPropertyChanged)

        self._activeMachineManager.activeMaterialChanged.connect(self._onMaterialChanged)
        #Application.getInstance().getController().getScene().sceneChanged.connect(self._onModelChanged)

        self._sceneRoot.childrenChanged.connect(self.connectTransformSignals)


    #
    #   CONFIRM/CANCEL PROPERTY CHANGES
    #
    def _onConfirmChanges(self):
        for prop in self._propertiesChanged:
            # Store changes to use case
            if prop is SmartSliceValidationProperty.FactorOfSafety:
                self._proxy._targetFactorOfSafety = self._proxy._changedValue
            elif prop is SmartSliceValidationProperty.MaxDisplacement:
                self._proxy._targetMaximalDisplacement = self._proxy._changedValue
            elif prop is SmartSliceValidationProperty.LoadMagnitude:
                self._proxy._loadMagnitude = self._proxy._changedValue
            elif prop is SmartSliceValidationProperty.LoadDirection:
                self._proxy._loadDirection = self._proxy._changedValue

          #  Face Selection
            elif prop is SmartSliceValidationProperty.SelectedFace:
                self._proxy.updateMeshes()
                self._proxy.selectedFacesChanged.emit()

          #  Material
            elif self._propertiesChanged[0] is SmartSliceValidationProperty.Material:
                self._material = self._changedMaterial
                self._material = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.MeshScale:
                self.meshScale = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.MeshRotation:
                self.meshRotation = self._changedValues.pop(0)
        
          # Shell Properties
            elif prop is SmartSliceValidationProperty.WallThickness:
                self.wallThickness = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallLineCount:
                self.wallLineCount = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallOuterWipeDistance:
                self.wallOuterWipeDist = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallTopSkinLayers:
                self.wallRoofingLayers = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallTopThickness:
                self.wallTopThickness = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallTopLayers:
                self.wallTopLayers = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallBottomThickness:
                self.wallBottomThickness = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallBottomLayers:
                self.wallBottomLayers = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallTopBottomPattern:
                self.wallTopBottomPattern = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallBottomInitialPattern:
                self.wallBottomInitialPattern = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallTopSkinLayers:
                self.wallSkinAngles = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallOuterInset:
                self.wallOuterInset = self._changedValues.pop(0)

          #  Infill Properties
            elif prop is SmartSliceValidationProperty.InfillDensity:
                self.infillDensity = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillLineDistance:
                self.infillLineDistance = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillPattern:
                self.infillPattern = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillAngles:
                self.infillLineDirection = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillOffsetX:
                self.infillOffsetX = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillOffsetY:
                self.infillOffsetY = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillLineMultiplier:
                self.infillMultiplier = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillOverlapPer:
                self.infillOverlapPercentage = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillOverlapMM:
                self.infillOverlapMM = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillWipeDistance:
                self.infillWipeDist = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillLayerThickness:
                self.infillLayerThick = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillGradualSteps:
                self.infillGradSteps = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillBeforeWalls:
                self.infillBeforeWalls = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillMinimumArea:
                self.infillMinimumArea = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillSupport:
                self.infillSupport = self._changedValues.pop(0)
          #  Skins
            elif prop is SmartSliceValidationProperty.SkinRemovalWidth:
                self.skinRemovalWidth = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.SkinTopRemovalWidth:
                self.skinRemovalTop = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.SkinBottomRemovalWidth:
                self.skinRemovalBottom = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.SkinExpandDistance:
                self.skinExpandDistance = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.SkinTopExpandDistance:
                self.skinExpandTop = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.SkinBottomExpandDistance:
                self.skinExpandBottom = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.SkinMaxAngleExpansion:
                self.skinExpandMaxAngle = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.SkinMinWidthExpansion:
                self.skinExpandMinWidth = self._changedValues.pop(0)

          #  Layer Height/Width
            elif prop is SmartSliceValidationProperty.LayerHeight:
                self.layerHeight = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InitialLayerHeight:
                self.layerHeightInitial = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.LineWidth:
                self.lineWidth = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.WallLineWidth:
                self.lineWidthWall = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.OuterLineWidth:
                self.lineWidthOuter = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InnerLineWidth:
                self.lineWidthInner = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.InfillLineWidth:
                self.lineWidthInfill = self._changedValues.pop(0)

            self._propertiesChanged.pop(0)


    def _onCancelChanges(self):
        for prop in self._propertiesChanged:
          #  REQUIREMENTS
            #  Factor of Safety (DEPRECATED)
            if prop is SmartSliceValidationProperty.FactorOfSafety:
                self._proxy.targetFactorOfSafetyChanged.emit()
            #  Max Displacement (DEPRECATED)
            elif prop is SmartSliceValidationProperty.MaxDisplacement:
                self._proxy.targetMaximalDisplacementChanged.emit()

            elif prop is SmartSliceValidationProperty.MeshScale:
                self.setMeshScale()
            elif prop is SmartSliceValidationProperty.MeshRotation:
                self.setMeshRotation()
                
          #  LOADS / ANCHORS
            #  Load Magnitude
            elif prop is SmartSliceValidationProperty.LoadMagnitude:
                self._proxy.loadMagnitudeChanged.emit()
            #  Load Direction
            elif prop is SmartSliceValidationProperty.LoadDirection:
                self._proxy.loadMagnitudeInvertedChanged.emit()
          #  FACE SELECTION
            #  Selected Face(s)
                # Do Nothing
        
          #  AIR QUALITY
            elif prop is SmartSliceValidationProperty.LayerHeight:
                self.setLayerHeight()
            elif prop is SmartSliceValidationProperty.InitialLayerHeight:
                self.setInitialLayerHeight()
            elif prop is SmartSliceValidationProperty.LineWidth:
                self.setLineWidth()
            elif prop is SmartSliceValidationProperty.WallLineWidth:
                self.setWallLineWidth()
            elif prop is SmartSliceValidationProperty.OuterLineWidth:
                self.setOuterLineWidth()
            elif prop is SmartSliceValidationProperty.InnerLineWidth:
                self.setInnerLineWidth()
            elif prop is SmartSliceValidationProperty.InfillLineWidth:
                self.setInfillLineWidth()

          #  SHELL
            elif prop is SmartSliceValidationProperty.LayerHeight:
                self.setLayerHeight()
            elif prop is SmartSliceValidationProperty.WallThickness:
                self.setWallThickness()
            elif prop is SmartSliceValidationProperty.WallOuterWipeDistance:
                self.setWallOuterWipeDist()
            elif prop is SmartSliceValidationProperty.WallTopSkinLayers:
                self.setWallRoofingLayerCount()
            elif prop is SmartSliceValidationProperty.WallLineCount:
                self.setWallLineCount()
            elif prop is SmartSliceValidationProperty.HorizontalExpansion:
                self.setHorizontalExpansion()
            elif prop is SmartSliceValidationProperty.WallTopThickness:
                self.setWallTopThickness()
            elif prop is SmartSliceValidationProperty.WallTopLayers:
                self.setWallTopLayers()
            elif prop is SmartSliceValidationProperty.WallBottomThickness:
                self.setWallBottomThickness()
            elif prop is SmartSliceValidationProperty.WallBottomLayers:
                self.setWallBottomLayers()
            elif prop is SmartSliceValidationProperty.WallTopBottomPattern:
                self.setWallTopBottomPattern()
            elif prop is SmartSliceValidationProperty.WallBottomInitialPattern:
                self.setWallBottomInitialPattern()
            elif prop is SmartSliceValidationProperty.WallTopSkinLayers:
                self.setWallSkinAngles()
            elif prop is SmartSliceValidationProperty.WallOuterInset:
                self.setWallOuterInset()

        
          #  INFILL PROPERTIES
            elif prop is SmartSliceValidationProperty.InfillDensity:
                self.setInfillDensity()
            elif prop is SmartSliceValidationProperty.InfillLineDistance:
                self.setInfillLineDistance()
            elif prop is SmartSliceValidationProperty.InfillPattern:
                self.setInfillPattern()
            elif prop is SmartSliceValidationProperty.InfillOffsetX:
                self.setInfillOffsetX()
            elif prop is SmartSliceValidationProperty.InfillOffsetY:
                self.setInfillOffsetY()
            elif prop is SmartSliceValidationProperty.InfillLineMultiplier:
                self.setInfillMultiplier()
            elif prop is SmartSliceValidationProperty.InfillOverlapPer:
                self.setInfillOverlap()
            elif prop is SmartSliceValidationProperty.InfillOverlapMM:
                self.setInfillOverlapMM()
            elif prop is SmartSliceValidationProperty.InfillWipeDistance:
                self.setInfillWipeDist()
            elif prop is SmartSliceValidationProperty.InfillLayerThickness:
                self.setInfillLayerThickness()
            elif prop is SmartSliceValidationProperty.InfillGradualSteps:
                self.setInfillGradualSteps()
            elif prop is SmartSliceValidationProperty.InfillBeforeWalls:
                self.setInfillBeforeWalls()
            elif prop is SmartSliceValidationProperty.InfillMinimumArea:
                self.setInfillMinimumArea()
            elif prop is SmartSliceValidationProperty.InfillSupport:
                self.setInfillSupport()
                    #  SKIN PROPERTIES
            elif prop is SmartSliceValidationProperty.SkinRemovalWidth:
                self.setSkinRemovalWidth()
            elif prop is SmartSliceValidationProperty.SkinTopRemovalWidth:
                self.setSkinRemovalTop()
            elif prop is SmartSliceValidationProperty.SkinBottomRemovalWidth:
                self.setSkinRemovalBottom()
            elif prop is SmartSliceValidationProperty.SkinExpandDistance:
                self.setSkinExpandDistance()
            elif prop is SmartSliceValidationProperty.SkinTopExpandDistance:
                self.setSkinExpandTop()
            elif prop is SmartSliceValidationProperty.SkinBottomExpandDistance:
                self.setSkinExpandBottom()
            elif prop is SmartSliceValidationProperty.SkinMaxAngleExpansion:
                self.setSkinMaxAngleExpansion()
            elif prop is SmartSliceValidationProperty.SkinMinWidthExpansion:
                self.setSkinMinWidthExpansion()

            #  Material Properties
            elif prop is SmartSliceValidationProperty.Material:
                self.setMaterial()

            self._propertiesChanged.pop(0)
        
        for i in self._changedValues:
            self._changedValues.pop(0)



    #
    #  LOCAL TRANSFORMATION PROPERTIES
    #

    def connectTransformSignals(self, dummy):
        i = 0
        _root = self._sceneRoot 

        for node in _root.getAllChildren():
            print ("Node Found:  " + node.getName())
            if node.getName() == "3d":
                if (self._sceneNode is None) or (self._sceneNode.getName() != _root.getAllChildren()[i+1].getName()):
                    self._sceneNode = _root.getAllChildren()[i+1]
                    print ("\nFile Found:  " + self._sceneNode.getName() + "\n")

                    #  Set Initial Scale/Rotation
                    self.meshScale    = self._sceneNode.getScale()
                    self.meshRotation = self._sceneNode.getOrientation()

                    #  TODO: Properly Disconnect this Signal, when figure out where to do so
                    self._sceneNode.transformationChanged.connect(self._onLocalTransformationChanged)
                    i += 1


            i += 1

        # STUB
        return 

    def _onLocalTransformationChanged(self, node):
        if node.getScale() != self.meshScale:
            self.onMeshScaleChanged()
        if node.getOrientation() != self.meshRotation:
            self.onMeshRotationChanged()

    def setMeshScale(self):
        print ("\nMesh Scale Set\n")
        self._sceneNode.setScale(self.meshScale)
        self._sceneNode.transformationChanged.emit(self._sceneNode)
        

    def onMeshScaleChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.MeshScale)
            self._changedValues.append(self._sceneNode.getScale())
            self.connector._confirmValidation()
        else:
            self.meshScale = self._sceneNode.getScale()

    def setMeshRotation(self):
        print ("\nMesh Rotation Set\n")
        self._sceneNode.setOrientation(self.meshRotation)
        self._sceneNode.transformationChanged.emit(self._sceneNode)

    def onMeshRotationChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.MeshRotation)
            self._changedValues.append(self._sceneNode.getOrientation())
            self.connector._confirmValidation()
        else:
            self.meshRotation = self._sceneNode.getOrientation()




    #
    #   QUALITY PROPERTIES
    #


    #
    #   SHELL PROPERTIES
    #

    #  Alternate Extra Wall (DISFUNCT)
    def setAlternateExtraWall(self):
        self._activeExtruder.setProperty("alternate_extra_perimeter", "value", self.alternateExtraWall)

    def onAlternateExtraWallChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.AlternateExtraWall)
            self._changedValues.append(self._activeExtruder.getProperty("alternate_extra_perimeter", "value"))
            self.connector._confirmValidation()
        else:
            self.alternateExtraWall = self._activeExtruder.getProperty("alternate_extra_perimeter", "value")

    #
    #   SHELL PROPERTIES
    #

    def setLayerHeight(self):
        self._activeMachineManager._global_container_stack.setProperty("layer_height", "value", self.layerHeight)

    def onLayerHeightChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.LayerHeight)
            self._changedValues.append(self._activeMachineManager._global_container_stack.getProperty("layer_height", "value"))
            self.connector._confirmValidation()
        else:
            self.layerHeight = self._activeMachineManager._global_container_stack.getProperty("layer_height", "value")

    def setInitialLayerHeight(self):
        self._activeExtruder.setProperty("initial_layer_height", "value", self.layerHeightInitial)

    def onInitialLayerHeightChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InitialLayerHeight)
            self._changedValues.append(self._activeExtruder.getProperty("initial_layer_height", "value"))
            self.connector._confirmValidation()
        else:
            self.layerHeightInitial = self._activeExtruder.getProperty("initial_layer_height", "value")

    def onInitialLayerLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InitialLayerLineWidth)
            self._changedValues.append(self._activeExtruder.getProperty("initial_layer_line_width", "value"))
            self.connector._confirmValidation()
        else:
            self.lineWidthInitialLayer = self._activeExtruder.getProperty("initial_layer_line_width", "value")


    def setLineWidth(self):
        self._activeExtruder.setProperty("line_width", "value", self.lineWidth)

    def onLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.LineWidth)
            self._changedValues.append(self._activeExtruder.getProperty("line_width", "value"))
            self.connector._confirmValidation()
        else:
            self.lineWidth = self._activeExtruder.getProperty("line_width", "value")

    def setWallLineWidth(self):
        self._activeExtruder.setProperty("wall_line_width", "value", self.lineWidthWall)

    def onWallLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallLineWidth)
            self._changedValues.append(self._activeExtruder.getProperty("wall_line_width", "value"))
            self.connector._confirmValidation()
        else:
            self.lineWidthWall = self._activeExtruder.getProperty("wall_line_width", "value")
        

    def setOuterLineWidth(self):
        self._activeExtruder.setProperty("wall_line_width_0", "value", self.lineWidthOuter)

    def onOuterLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.OuterLineWidth)
            self._changedValues.append(self._activeExtruder.getProperty("wall_line_width_0", "value"))
            self.connector._confirmValidation()
        else:
            self.lineWidthOuter = self._activeExtruder.getProperty("wall_line_width_0", "value")

    def setInnerLineWidth(self):
        self._activeExtruder.setProperty("wall_line_width_x", "value", self.lineWidthInner)

    def onInnerLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InnerLineWidth)
            self._changedValues.append(self._activeExtruder.getProperty("wall_line_width_x", "value"))
            self.connector._confirmValidation()
        else:
            self.lineWidthInner = self._activeExtruder.getProperty("wall_line_width_x", "value")

    def setInfillLineWidth(self):
        self._activeExtruder.setProperty("infill_line_width", "value", self.lineWidthInfill)

    def onInfillLineWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillLineWidth)
            self._changedValues.append(self._activeExtruder.getProperty("infill_line_width", "value"))
            self.connector._confirmValidation()
        else:
            self.lineWidthInfill = self._activeExtruder.getProperty("infill_line_width", "value")

    #
    #   SHELLS
    #
    def setWallThickness(self):
        self._activeExtruder.setProperty("wall_thickness", "value", self.wallThickness)

    def onWallThicknessChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallThickness)
            self._changedValues.append(self._activeExtruder.getProperty("wall_thickness", "value"))
            self.connector._confirmValidation()
        else:
            self.wallThickness = self._activeExtruder.getProperty("wall_thickness", "value")

    def setWallLineCount(self):
        self._activeExtruder.setProperty("wall_line_count", "value", self.wallLineCount)

    def onWallLineCountChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallLineCount)
            self._changedValues.append(self._activeExtruder.getProperty("wall_line_count", "value"))
            self.connector._confirmValidation()
        else:
            self.wallLineCount = self._activeExtruder.getProperty("wall_line_count", "value")

    def setWallOuterWipeDist(self):
        self._activeExtruder.setProperty("wall_0_wipe_dist", "value", self.wallOuterWipeDist)

    def onWallOuterWipeDistChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallOuterWipeDistance)
            self._changedValues.append(self._activeExtruder.getProperty("wall_0_wipe_dist", "value"))
            self.connector._confirmValidation()
        else:
            self.wallOuterWipeDist = self._activeExtruder.getProperty("wall_0_wipe_dist", "value")

    def setWallRoofingLayerCount(self):
        self._activeExtruder.setProperty("roofing_layer_count", "value", self.wallRoofingLayers)

    def onWallRoofingLayerCountChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallTopSkinLayers)
            self._changedValues.append(self._activeExtruder.getProperty("roofing_layer_count", "value"))
            self.connector._confirmValidation()
        else:
            self.wallRoofingLayers = self._activeExtruder.getProperty("roofing_layer_count", "value")

    def setWallTopThickness(self):
        self._activeExtruder.setProperty("top_thickness", "value", self.wallTopThickness)

    def onWallTopThicknessChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallTopThickness)
            self._changedValues.append(self._activeExtruder.getProperty("top_thickness", "value"))
            self.connector._confirmValidation()
        else:
            self.wallTopThickness = self._activeExtruder.getProperty("top_thickness", "value")

    def setWallTopLayers(self):
        self._activeExtruder.setProperty("top_layers", "value", self.wallTopLayers)

    def onWallTopLayersChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallTopLayers)
            self._changedValues.append(self._activeExtruder.getProperty("top_layers", "value"))
            self.connector._confirmValidation()
        else:
            self.wallTopLayers = self._activeExtruder.getProperty("top_layers", "value")

    def setWallBottomThickness(self):
        self._activeExtruder.setProperty("bottom_thickness", "value", self.wallBottomThickness)

    def onWallBottomThicknessChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallBottomThickness)
            self._changedValues.append(self._activeExtruder.getProperty("bottom_thickness", "value"))
            self.connector._confirmValidation()
        else:
            self.wallBottomThickness = self._activeExtruder.getProperty("bottom_thickness", "value")
        
    def setWallBottomLayers(self):
        self._activeExtruder.setProperty("bottom_layers", "value", self.wallBottomLayers)

    def onWallBottomLayersChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallBottomLayers)
            self._changedValues.append(self._activeExtruder.getProperty("bottom_layers", "value"))
            self.connector._confirmValidation()
        else:
            self.wallBottomLayers = self._activeExtruder.getProperty("bottom_layers", "value")

    def setWallTopBottomPattern(self):
        self._activeExtruder.setProperty("top_bottom_pattern", "value", self.wallTopBottomPattern)

    def onWallTopBottomPatternChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallTopBottomPattern)
            self._changedValues.append(self._activeExtruder.getProperty("top_bottom_pattern", "value"))
            self.connector._confirmValidation()
        else:
            self.wallTopBottomPattern = self._activeExtruder.getProperty("top_bottom_pattern", "value")

    def setWallBottomInitialPattern(self):
        self._activeExtruder.setProperty("top_bottom_pattern_0", "value", self.wallBottomInitialPattern)

    def onWallBottomInitialPatternChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallBottomInitialPattern)
            self._changedValues.append(self._activeExtruder.getProperty("top_bottom_pattern_0", "value"))
            self.connector._confirmValidation()
        else:
            self.wallBottomInitialPattern = self._activeExtruder.getProperty("top_bottom_pattern_0", "value")

    def setWallSkinAngles(self):
        self._activeExtruder.setProperty("skin_angles", "value", self.wallSkinAngles)

    def onWallSkinAnglesChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.SkinAngles)
            self._changedValues.append(self._activeExtruder.getProperty("skin_angles", "value"))
            self.connector._confirmValidation()
        else:
            self.wallSkinAngles = self._activeExtruder.getProperty("skin_angles", "value")

    def setWallOuterInset(self):
        self._activeExtruder.setProperty("wall_0_inset", "value", self.wallOuterInset)

    def onWallOuterInsetChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.WallOuterInset)
            self._changedValues.append(self._activeExtruder.getProperty("wall_0_inset", "value"))
            self.connector._confirmValidation()
        else:
            self.wallOuterInset = self._activeExtruder.getProperty("wall_0_inset", "value")





    #
    #   INFILL PROPERTIES
    #

    #  Infill Line Distance
    def setInfillLineDistance(self):
        self._activeExtruder.setProperty("infill_line_distance", "value", self.infillLineDistance)

    def onInfillLineDistanceChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillLineDistance)
            self._changedValues.append(self._activeExtruder.getProperty("infill_line_distance", "value"))
            self.connector._confirmValidation()
        else:
            self.infillLineDistance = self._activeExtruder.getProperty("infill_line_distance", "value")

    #  Infill Angles
    def setInfillAngles(self):
        self._activeExtruder.setProperty("infill_angles", "value", self.infillLineDirection)

    def onInfillAnglesChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillAngles)
            self._changedValues.append(self._activeExtruder.getProperty("infill_angles", "value"))
            self.connector._confirmValidation()
        else:
            self.infillLineDirection = self._activeExtruder.getProperty("infill_angles", "value")

    def setInfillDensity(self):
        self._activeExtruder.setProperty("infill_sparse_density", "value", self.infillDensity)

    def onInfillDensityChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillDensity)
            self._changedValues.append(self._activeExtruder.getProperty("infill_sparse_density", "value"))
            self.connector._confirmValidation()
        else:
            self.infillDensity = self._activeExtruder.getProperty("infill_sparse_density", "value")

    def setInfillPattern(self):
        self._activeExtruder.setProperty("infill_pattern", "value", self.infillPattern)

    def onInfillPatternChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillPattern)
            self._changedValues.append(self._activeExtruder.getProperty("infill_pattern", "value"))
            self.connector._confirmValidation()
        else:
            self.infillPattern = self._activeExtruder.getProperty("infill_pattern", "value")

    def setInfillOffsetX(self):
        self._activeExtruder.setProperty("infill_offset_x", "value", self.infillOffsetX)

    def onInfillOffsetXChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillOffsetX)
            self._changedValues.append(self._activeExtruder.getProperty("infill_offset_x", "value"))
            self.connector._confirmValidation()
        else:
            self.infillOffsetX = self._activeExtruder.getProperty("infill_offset_x", "value")

    def setInfillOffsetY(self):
        self._activeExtruder.setProperty("infill_offset_y", "value", self.infillOffsetY)

    def onInfillOffsetYChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillOffsetY)
            self._changedValues.append(self._activeExtruder.getProperty("infill_offset_y", "value"))
            self.connector._confirmValidation()
        else:
            self.infillOffsetY = self._activeExtruder.getProperty("infill_offset_y", "value")

    def setInfillMultiplier(self):
        self._activeExtruder.setProperty("infill_muliplier", "value", self.infillMultiplier)

    def onInfillMultiplierChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillLineMultiplier)
            self._changedValues.append(self._activeExtruder.getProperty("infill_multiplier", "value"))
            self.connector._confirmValidation()
        else:
            self.infillMultiplier = self._activeExtruder.getProperty("infill_multiplier", "value")

    def setInfillOverlap(self):
        self._activeExtruder.setProperty("infill_overlap", "value", self.infillOverlapPercentage)

    def onInfillOverlapChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillOverlapPer)
            self_changedValues.append(self._activeExtruder.getProperty("infill_overlap", "value"))
            self.connector._confirmValidation()
        else:
            self.infillOverlapPercentage = self._activeExtruder.getProperty("infill_overlap", "value")

    def setInfillOverlapMM(self):
        self._activeExtruder.setProperty("infill_overlap_mm", "value", self.infillOverlapMM)

    def onInfillOverlapMMChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillOverlapMM)
            self._changedValues.append(self._activeExtruder.getProperty("infill_overlap_mm", "value"))
            self.connector._confirmValidation()
        else:
            self.infillOverlapMM = self._activeExtruder.getProperty("infill_overlap_mm", "value")

    def setInfillWipeDist(self):
        self._activeExtruder.setProperty("infill_wipe_dist", "value", self.infillWipeDist)

    def onInfillWipeDistChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillWipeDistance)
            self._changedValues.append(self._activeExtruder.getProperty("infill_wipe_dist", "value"))
            self.connector._confirmValidation()
        else:
            self.infillWipeDist = self._activeExtruder.getProperty("infill_wipe_dist", "value")
        
    def setInfillLayerThickness(self):
        self._activeExtruder.setProperty("infill_sparse_thickness", "value", self.infillLayerThick)

    def onInfillLayerThicknessChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillLayerThickness)
            self._changedValues.append(self._activeExtruder.getProperty("infill_sparse_thickness", "value"))
            self.connector._confirmValidation()
        else:
            self.infillLayerThick = self._activeExtruder.getProperty("infill_sparse_thickness", "value")

    def setInfillGradualSteps(self):
        self._activeExtruder.setProperty("gradual_infill_steps", "value", self.infillGradSteps)
    
    def onInfillGradualStepsChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillGradualSteps)
            self._changedValues.append(self._activeExtruder.getProperty("gradual_infill_steps", "value"))
            self.connector._confirmValidation()
        else:
            self.infillGradSteps = self._activeExtruder.getProperty("gradual_infill_steps", "value")

    def setInfillBeforeWalls(self):
        self._activeExtruder.setProperty("infill_before_walls", "value", self.infillBeforeWalls)

    def onInfillBeforeWalls(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillBeforeWalls)
            self._changedValues.append(self._activeExtruder.getProperty("infill_before_walls", "value"))
            self.connector._confirmValidation()
        else:
            self.infillBeforeWalls = self._activeExtruder.getProperty("infill_before_walls", "value")

    def setInfillMinimumArea(self):
        self._activeExtruder.setProperty("min_infill_area", "value", self.infillMinimumArea)
    
    def onInfillMinAreaChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillMinimumArea)
            self._changedValues.append(self._activeExtruder.getProperty("min_infill_area", "value"))
            self.connector._confirmValidation()
        else:
            self.infillMinimumArea = self._activeExtruder.getProperty("min_infill_area", "value")

    def setInfillSupport(self):
        self._activeExtruder.setProperty("infill_support_enabled", "value", self.infillSupport)

    def onInfillSupportChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.InfillSupport)
            self._changedValues.append(self._activeExtruder.getProperty("infill_support_enabled", "value"))
            self.connector._confirmValidation()
        else:
            self.infillSupport = self._activeExtruder.getProperty("infill_support_enabled", "value")

    def setSkinRemovalWidth(self):
        self._activeExtruder.setProperty("skin_preshrink", "value", self.skinRemovalWidth)

    def onSkinRemovalWidthChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.SkinRemovalWidth)
            self._changedValues.append(self._activeExtruder.getProperty("skin_preshrink", "value"))
            self.connector._confirmValidation()
        else:
            self.skinRemovalWidth = self._activeExtruder.getProperty("skin_preshrink", "value")

    def setSkinRemovalTop(self):
        self._activeExtruder.setProperty("top_skin_preshrink", "value", self.skinRemovalTop)

    def onSkinRemovalTopChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.SkinTopRemovalWidth)
            self._changedValues.append(self._activeExtruder.getProperty("top_skin_preshrink", "value"))
            self.connector._confirmValidation()
        else:
            self.skinRemovalTop = self._activeExtruder.getProperty("top_skin_preshrink", "value")

    def setSkinRemovalBottom(self):
        self._activeExtruder.setProperty("bottom_skin_preshrink", "value", self.skinRemovalBottom)

    def onSkinRemovalBottomChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.SkinBottomRemovalWidth)
            self._changedValues.append(self._activeExtruder.getProperty("bottom_skin_preshrink", "value"))
            self.connector._confirmValidation()
        else:
            self.skinRemovalBottom = self._activeExtruder.getProperty("bottom_skin_preshrink", "value")

    def setSkinExpandDistance(self):
        self._activeExtruder.setProperty("expand_skins_expand_distance", "value", self.skinExpandDistance)

    def onSkinExpandDistanceChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.SkinExpandDistance)
            self._changedValues.append(self._activeExtruder.getProperty("expand_skins_expand_distance", "value"))
            self.connector._confirmValidation()
        else:
            self.skinExpandDistance = self._activeExtruder.getProperty("expand_skins_expand_distance", "value")

    def setSkinExpandTop(self):
        self._activeExtruder.setProperty("top_skin_expand_distance", "value", self.skinExpandTop)

    def onSkinExpandTopChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.SkinTopExpandDistance)
            self._changedValues.append(self._activeExtruder.getProperty("top_skin_expand_distance", "value"))
            self.connector._confirmValidation()
        else:
            self.skinExpandTop = self._activeExtruder.getProperty("top_skin_expand_distance", "value")

    def setSkinExpandBottom(self):
        self._activeExtruder.setProperty("bottom_skin_expand_distance", "value", self.skinExpandBottom)

    def onSkinExpandBottomChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.SkinBottomExpandDistance)
            self._changedValues.append(self._activeExtruder.getProperty("bottom_skin_expand_distance", "value"))
            self.connector._confirmValidation()
        else:
            self.skinExpandBottom = self._activeExtruder.getProperty("bottom_skin_expand_distance", "value")

    def setSkinMaxAngleExpansion(self):
        self._activeExtruder.setProperty("max_skin_angle_for_expansion", "value", self.skinExpandMaxAngle)

    def onSkinMaxAngleExpansionChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.SkinMaxAngleExpansion)
            self._changedValues.append(self._activeExtruder.getProperty("max_skin_angle_for_expansion", "value"))
            self.connector._confirmValidation()
        else:
            self.skinExpandMaxAngle = self._activeExtruder.getProperty("max_skin_angle_for_expansion", "value")

    def setSkinMinWidthExpansion(self):
        self._activeExtruder.setProperty("min_skin_width_for_expansion", "value", self.skinExpandMinWidth)

    def onSkinMinAngleExpansionChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.SkinMinWidthExpansion)
            self._changedValues.append(self._activeExtruder.getProperty("min_skin_width_for_expansion", "value"))
            self.connector._confirmValidation()
        else:
            self.skinExpandMinWidth = self._activeExtruder.getProperty("min_skin_width_for_expansion", "value")


    def onTopLineDirectionChanged(self):
        #  STUB 
        1 + 1

    def onBottomLineDirectionChanged(self):
        #  STUB 
        1 + 1
    

    #
    #   MATERIAL CHANGES
    #
    activeMaterialChanged = pyqtSignal()

    def setMaterial(self):
       self._activeExtruder.material = self._material
       

    def _onMaterialChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            #print("\n\nMATERIAL CHANGE CONFIRMED HERE\n\n")
            self._propertiesChanged.append(SmartSliceValidationProperty.Material)
            self._changedValues.append(self._activeExtruder.material)
            self.connector._confirmValidation()
        else:
            #print("\n\nMATERIAL CHANGED HERE\n\n")
            self._material = self._activeExtruder.material


    #
    #   SIGNAL LISTENERS
    #

    # On GLOBAL Property Changed
    def _onGlobalPropertyChanged(self, key: str, property_name: str):

        if   key == "layer_height" and property_name == "value":          
            self.onLayerHeightChanged()
        elif key == "initial_layer_height" and property_name == "value":   
            self.onInitialLayerHeightChanged()

        else: 
            return

    # On EXTRUDER Property Changed
    def _onExtruderPropertyChanged(self, key: str, property_name: str):
        
      #  Infills
        if   key == "infill_sparse_density" and property_name == "value":
            self.onInfillDensityChanged()
        elif key == "infill_line_distance" and property_name == "value":
            self.onInfillLineDistanceChanged()
        elif key == "infill_pattern" and property_name == "value":
            self.onInfillPatternChanged()
        elif key == "infill_multiplier" and property_name == "value":
            self.onInfillMultiplierChanged()
        elif key == "infill_offset_x" and property_name == "value":
            self.onInfillOffsetXChanged()
        elif key == "infill_offset_y" and property_name == "value":
            self.onInfillOffsetYChanged()
        elif key == "infill_overlap" and property_name == "value":
            self.onInfillOverlapChanged()
        elif key == "infill_overlap_mm" and property_name == "value":
            self.onInfillOverlapMMChanged()
        elif key == "infill_wipe_dist" and property_name == "value":
            self.onInfillWipeDistChanged()
        elif key == "infill_sparse_thickness" and property_name == "value":
            self.onInfillLayerThicknessChanged()
        elif key == "gradual_infill_steps" and property_name == "value":
            self.onInfillGradualStepsChanged()
        elif key == "infill_before_walls" and property_name == "value":
            self.onInfillBeforeWalls()
        elif key == "min_infill_area" and property_name == "value":
            self.onInfillMinAreaChanged()
        elif key == "infill_support_enabled" and property_name == "value":
            self.onInfillSupportChanged()
      #  Skins
        elif key == "skin_preshrink" and property_name == "value":
            self.onSkinRemovalWidthChanged()
        elif key == "top_skin_preshrink" and property_name == "value":
            self.onSkinRemovalTopChanged()
        elif key == "bottom_skin_preshrink" and property_name == "value":
            self.onSkinRemovalBottomChanged()
        elif key == "expand_skins_expand_distance" and property_name == "value":
            self.onSkinExpandDistanceChanged()
        elif key == "top_skin_expand_distance" and property_name == "value":
            self.onSkinExpandTopChanged()
        elif key == "bottom_skin_expand_distance" and property_name == "value":
            self.onSkinExpandBottomChanged()
        elif key == "max_skin_angle_for_expansion" and property_name == "value":
            self.onSkinMaxAngleExpansionChanged()
        elif key == "min_skin_angle_for_expansion" and property_name == "value":
            self.onSkinMinAngleExpansionChanged()
        
        elif key == "line_width" and property_name == "value":
            self.onLineWidthChanged()
        elif key == "wall_line_width" and property_name == "value":
            self.onOuterLineWidthChanged()
        elif key == "wall_line_width" and property_name == "value":
            self.onInnerLineWidthChanged()
        elif key == "infill_wall_line_width" and property_name == "value":
            self.onInfillLineWidthChanged()
        
        elif key == "wall_thickness" and property_name == "value":
            self.onWallThicknessChanged()
        elif key == "wall_line_count" and property_name == "value":
            self.onWallLineCountChanged()
        elif key == "wall_0_wipe_dist" and property_name == "value":
            self.onWallOuterWipeDistChanged()
        elif key == "roofing_layer_count" and property_name == "value":
            self.onWallRoofingLayerCountChanged()
        elif key == "top_thickness" and property_name == "value":
            self.onWallTopThicknessChanged()
        elif key == "top_layers" and property_name == "value":
            self.onWallTopLayersChanged()
        elif key == "bottom_thickness" and property_name == "value":
            self.onWallBottomThicknessChanged()
        elif key == "bottom_layers" and property_name == "value":
            self.onWallBottomLayersChanged()
        elif key == "horizontal_expansion" and property_name == "value":    # DISFUNCT!!!!
            self.onHorizontalExpansionChanged()
        elif key == "top_bottom_pattern" and property_name == "value":
            self.onWallTopBottomPatternChanged()
        elif key == "top_bottom_pattern_0" and property_name == "value":
            self.onWallBottomInitialPatternChanged()
        elif key == "skin_angles" and property_name == "value":
            self.onWallSkinAnglesChanged()
        elif key == "wall_0_inset" and property_name == "value":
            self.onWallOuterInsetChanged()

        #  Other Property
        else:
            return

