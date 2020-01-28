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
from UM.Preferences import Preferences
from UM.Settings.ContainerStack import ContainerStack
from UM.Scene.Selection import Selection
from UM.Logger import Logger
from cura.CuraApplication import CuraApplication
from cura.Settings.SettingOverrideDecorator import SettingOverrideDecorator


#  Smart Slice
from .SmartSliceCloudProxy import SmartSliceCloudStatus
from .SmartSliceValidationProperty import SmartSliceValidationProperty, SmartSliceLoadDirection

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
        self._hasChanges = False

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
        self._selection_mode = 1 # Default to AnchorMode
        self._changedMesh = None
        self._changedFaces = None
        self._changedForce = None
        self._anchoredMesh = None
        self._anchoredFaces = None
        self._loadedMesh = None
        self._loadedFaces = None
        self._sceneNode = None
        self._sceneRoot = Application.getInstance().getController().getScene().getRoot()

        self._material = self._activeMachineManager._global_container_stack.extruderList[0].material #  Cura Material Node

        self._cancelChanges = False
        
        #  Connect Signals
        global_stack.propertyChanged.connect(self._onGlobalPropertyChanged)
        self._activeExtruder.propertyChanged.connect(self._onExtruderPropertyChanged)

        self._activeMachineManager.activeMaterialChanged.connect(self._onMaterialChanged)
        #Application.getInstance().getController().getScene().sceneChanged.connect(self._onModelChanged)

        self._sceneRoot.childrenChanged.connect(self.connectMeshSignals)
        

        self._global_stack_id = global_stack.getId()
        self._extruder_stack_id = self._activeExtruder.getId()

        self._global_cache = None
        self._extruder_cache = None


    def cacheChanges(self):
        print ("\nTest Property Extruder:  " + str(self._activeExtruder.getProperty("infill_sparse_density", "value")) + "\n")

        self._global_cache   = Application.getInstance().getMachineManager().activeMachine.serialize()
        self._extruder_cache = self._activeExtruder.serialize()

    def restoreCache(self):
        test = ContainerStack(0)
        test.deserialize(self._extruder_cache)
        
        self._activeMachineManager.activeMachine.deserialize(self._global_cache)
        self._activeExtruder.deserialize(self._extruder_cache)

        print ("\nTest Property Cache:  " + str(test.getProperty("infill_sparse_density", "value")) + "\n")


    def cancelChanges(self):
        self.restoreCache()

    def confirmChanges(self):
        self.cacheChanges()


    #
    #   CONFIRM/CANCEL PROPERTY CHANGES
    #
    def _onConfirmChanges(self):
        for prop in self._propertiesChanged:
          #  Use-Case/Requirements
            if   prop is SmartSliceValidationProperty.MaxDisplacement:
                self.connector._proxy.reqsMaxDeflect = self.connector._proxy.targetMaximalDisplacement
            elif prop is SmartSliceValidationProperty.FactorOfSafety:
                self.connector._proxy.reqsSafetyFactor = self.connector._proxy.targetFactorOfSafety
            elif prop is SmartSliceValidationProperty.LoadDirection:
                self.connector._proxy.reqsLoadDirection = self.connector._proxy.loadDirection
            elif prop is SmartSliceValidationProperty.LoadMagnitude:
                self.connector._proxy.reqsLoadMagnitude = self.connector._proxy.loadMagnitude

          #  Face Selection
            elif prop is SmartSliceValidationProperty.SelectedFace:
                self.updateMeshes()
                self.selectedFacesChanged.emit()

          #  Material
            elif prop is SmartSliceValidationProperty.Material:
                self._material = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.MeshScale:
                self.meshScale = self._changedValues.pop(0)
            elif prop is SmartSliceValidationProperty.MeshRotation:
                self.meshRotation = self._changedValues.pop(0)
        
        self.confirmChanges()

        self.connector._proxy.confirmationWindowEnabled = False
        self.connector._proxy.confirmationWindowEnabledChanged.emit()


    def _onCancelChanges(self):
        self._cancelChanges = True
        self.cancelChanges()
        #Logger.log(str(prop))
        for prop in self._propertiesChanged:
            print (str(prop))
          #  REQUIREMENTS / USE-CASE
            if prop is SmartSliceValidationProperty.FactorOfSafety:
                self.connector._proxy.setFactorOfSafety()
            elif prop is SmartSliceValidationProperty.MaxDisplacement:
                self.connector._proxy.setMaximalDisplacement()
            elif prop is SmartSliceValidationProperty.LoadMagnitude:
                self.connector._proxy.setLoadMagnitude()
            elif prop is SmartSliceValidationProperty.LoadDirection:
                self.connector._proxy.setLoadDirection()

            elif prop is SmartSliceValidationProperty.MeshScale:
                self.setMeshScale()
            elif prop is SmartSliceValidationProperty.MeshRotation:
                self.setMeshRotation()

          #  FACE SELECTION
            #  Selected Face(s)
                # Do Nothing
        
            #  Material Properties
            elif prop is SmartSliceValidationProperty.Material:
                self.setMaterial()

            self._propertiesChanged.pop(0)

        
        for i in self._changedValues:
            self._changedValues.pop(0)
        self.connector._proxy.confirmationWindowEnabled = False
        self.connector._proxy.confirmationWindowEnabledChanged.emit()

        self._cancelChanges = False


    #
    #  LOCAL TRANSFORMATION PROPERTIES
    #

    def connectMeshSignals(self, dummy):
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
                    
                    #self._sceneNode.childrenChanged.connect(self._onMeshChildrenChanged)

                    #  TODO: Properly Disconnect this Signal, when figure out where to do so
                    self._sceneNode.transformationChanged.connect(self._onLocalTransformationChanged)
                    i += 1
            
            i += 1

        # STUB
        return 


    #
    #  LOCAL TRANSFORMATION
    #

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
        if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing):
            self._propertiesChanged.append(SmartSliceValidationProperty.MeshScale)
            self._changedValues.append(self._sceneNode.getScale())
            self.connector._confirmValidation()
        else:
            self.connector._prepareValidation()
            self.meshScale = self._sceneNode.getScale()

    def setMeshRotation(self):
        print ("\nMesh Rotation Set\n")
        self._sceneNode.setOrientation(self.meshRotation)
        self._sceneNode.transformationChanged.emit(self._sceneNode)

    def onMeshRotationChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing):
            self._propertiesChanged.append(SmartSliceValidationProperty.MeshRotation)
            self._changedValues.append(self._sceneNode.getOrientation())
            self.connector._confirmValidation()
        else:
            self.connector._prepareValidation()
            self.meshRotation = self._sceneNode.getOrientation()



    #
    #   MATERIAL CHANGES
    #
    activeMaterialChanged = pyqtSignal()

    def setMaterial(self):
       self._activeExtruder.material = self._material
       

    def _onMaterialChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing):
            #print("\n\nMATERIAL CHANGE CONFIRMED HERE\n\n")
            self._propertiesChanged.append(SmartSliceValidationProperty.Material)
            self._changedValues.append(self._activeExtruder.material)
            if len(self._propertiesChanged) > 2:
                print ("\nlength: " + str(len(self._propertiesChanged)) + "\n")
                self.connector._confirmValidation()
        else:
            #print("\n\nMATERIAL CHANGED HERE\n\n")
            #  TODO:  Next line is commented because there are two signals that are thrown
            #self.connector._prepareValidation()
            self._material = self._activeExtruder.material
            
    #
    #   FACE SELECTION
    #

    selectedFacesChanged = pyqtSignal() 

    def confirmFaceDraw(self, force=None):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating:
            self._propertiesChanged.append(SmartSliceValidationProperty.SelectedFace)
            self.connector._confirmValidation()
        else:
            self.connector._prepareValidation()
            self.updateMeshes()
            self.selectedFacesChanged.emit()

    def updateMeshes(self):
        #  ANCHOR MODE
        if self._selection_mode == 1:
            self._anchoredMesh = self._changedMesh
            self._anchoredFaces = self._changedFaces
        #  LOAD MODE
        else:
            self._loadedMesh = self._changedMesh
            self._loadedFaces = self._changedFaces



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
        if not self._cancelChanges:        
            if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing):
                #  Confirm Settings Changes
                self.connector._confirmValidation()
            else:
                self.connector._prepareValidation()
                #  Cache New Settings


    '''
      _onSceneNodesChanged()
        Executed when a node is changed relative to the root node.
        Confirms that only one sliceable model is connected to scene and
          reports any modifier meshes that are currently loaded for model
    '''
    def _onSceneNodesChanged(self, root):
        models = 0

        for node in root.getAllChildren():
            print ("Node Found:  " + node.getName())
            if node.getName() == "3d":
                if (self._sceneNode is None) or (self._sceneNode.getName() != root.getAllChildren()[i+1].getName()):
                    self._sceneNode = _root.getAllChildren()[i+1]
                    print ("\nFile Found:  " + self._sceneNode.getName() + "\n")

                    #  Set Initial Scale/Rotation
                    self.meshScale    = self._sceneNode.getScale()
                    self.meshRotation = self._sceneNode.getOrientation()
                    
                    #self._sceneNode.childrenChanged.connect(self._onMeshChildrenChanged)

                    #  TODO: Properly Disconnect this Signal, when figure out where to do so
                    self._sceneNode.transformationChanged.connect(self._onLocalTransformationChanged)
                    i += 1

            i += 1