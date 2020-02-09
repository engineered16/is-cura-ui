#   SmartSlicePropertyHandler.py
#   Teton Simulation
#   Authored on   January 3, 2019
#   Last Modified January 3, 2019

#
#  Contains procedures for handling Cura Properties in accordance with SmartSlice
#

import copy
from copy import copy

from asyncio import Lock

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import QObject

#  Cura
from UM.Application import Application
from UM.Preferences import Preferences
from UM.Settings.ContainerStack import ContainerStack
from UM.Scene.Selection import Selection
from UM.Signal import Signal
from UM.Logger import Logger
from cura.CuraApplication import CuraApplication
from cura.Settings.SettingOverrideDecorator import SettingOverrideDecorator
from UM.Settings.SettingInstance import InstanceState


#  Smart Slice
from .SmartSliceCloudProxy import SmartSliceCloudStatus
from .SmartSliceValidationProperty import SmartSliceValidationProperty, SmartSliceLoadDirection

class SmartSlicePropertyHandler(QObject):
    def __init__(self, connector):
        super().__init__()

        #  Callback
        self.connector = connector
        self._confirming = False
        self._initialized = False
        
        self._activeMachineManager = CuraApplication.getInstance().getMachineManager()
        self._globalStack = self._activeMachineManager.activeMachine
        self._activeExtruder = self._globalStack.extruderList[0]
        
        #  Cache Space
        self._propertiesChanged = []
        self._changedValues     = []
        self._hasChanges = False


        #  Mesh Properties
        self.meshScale = None
        self._newScale = None
        self.meshRotation = None
        self._newRotation = None


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
        self._cancellingChanges = Lock()
        
        #  Connect Signals
        self._globalStack.propertyChanged.connect(self._onGlobalPropertyChanged)
        self._activeExtruder.propertyChanged.connect(self._onExtruderPropertyChanged)

        self._activeMachineManager.activeMaterialChanged.connect(self._onMaterialChanged)
        #Application.getInstance().getController().getScene().sceneChanged.connect(self._onModelChanged)

        self._sceneRoot.childrenChanged.connect(self.connectMeshSignals)
        
        self._global_cache = {}
        self._extruder_cache = {}

        self.global_keys = {"layer_height_0", "layer_height"}

        self.extruder_keys = {"wall_line_width_0", "wall_line_width_x", "wall_line_width", "line_width", "wall_line_count", "wall_thickness", 
                         "skin_angles", "top_layers", "bottom_layers", 
                         "infill_pattern", "infill_sparse_density", "infill_angles", 
                         "alternate_extra_perimeter"}

    def clearChangedProperties(self):
        for p in self._propertiesChanged:
            self._propertiesChanged.pop()
        for i in self._changedValues:
            self._changedValues.pop()

    def cacheGlobal(self):

        self._global_cache = {}

        for key in self.global_keys:
            if key not in self._global_cache:
                self._global_cache[key] = self._globalStack.getProperty(key, "value")
            if self._global_cache[key] != self._globalStack.getProperty(key, "value"):
                self._global_cache[key] = self._globalStack.getProperty(key, "value")
                self.connector._proxy._confirmationWindowEnabled = False
                self.connector._proxy._confirmationWindowEnabledChanged.emit()
                #print ("\nSetting State:  " + str(self._globalStack.getProperty(key, "state")) + "\n")
            

    def cacheExtruder(self):

        self._extruder_cache = {}

        for key in self.extruder_keys:
            if key not in self._extruder_cache:
                self._extruder_cache[key] = self._activeExtruder.getProperty(key, "value")
            if self._extruder_cache[key] != self._activeExtruder.getProperty(key, "value"):
                self._extruder_cache[key] = self._activeExtruder.getProperty(key, "value")

    def cacheSmartSlice(self):
        i = 0
        for prop in self._propertiesChanged:
            if prop is SmartSliceValidationProperty.MaxDisplacement:
                self.connector._proxy.reqsMaxDeflect = self._changedValues[i]
                self.connector._proxy.setMaximalDisplacement()
            elif prop is SmartSliceValidationProperty.FactorOfSafety:
                self.connector._proxy.reqsSafetyFactor = self._changedValues[i]
                self.connector._proxy.setFactorOfSafety()
            elif prop is SmartSliceValidationProperty.LoadDirection:
                self.connector._proxy.reqsLoadDirection = self._changedValues[i]
                self.connector._proxy.setLoadDirection()
            elif prop is SmartSliceValidationProperty.LoadMagnitude:
                self.connector._proxy.reqsLoadMagnitude = self._changedValues[i]
                self.connector._proxy.setLoadMagnitude()

          #  Face Selection
            elif prop is SmartSliceValidationProperty.SelectedFace:
                self.updateMeshes()
                self.selectedFacesChanged.emit()

          #  Material
            elif prop is SmartSliceValidationProperty.Material:
                self._material = self._changedValues[i]
                self.setMaterial()
                self._propertiesChanged.pop()
            elif prop is SmartSliceValidationProperty.MeshScale:
                self.meshScale = self._newScale
                self.setMeshScale()
                self._newScale = self.meshScale
                self._propertiesChanged.pop()
            elif prop is SmartSliceValidationProperty.MeshRotation:
                self.meshRotation = self._newRotation
                self.setMeshRotation()
                self._newRotation = self.meshRotation
                self._propertiesChanged.pop()
            

            i += 0


        self.clearChangedProperties()

    def cacheChanges(self):
        self.cacheSmartSlice()
        self.cacheGlobal()
        self.cacheExtruder()

    def restoreCache(self):

        for property in self._global_cache:
            if self._global_cache[property] != self._globalStack.getProperty(property, "value"):
                self._globalStack.setProperty(property, "value", self._global_cache[property])
                #self._globalStack.setProperty(property, "state", InstanceState.Default)

        for property in self._extruder_cache:
            if self._extruder_cache[property] != self._activeExtruder.getProperty(property, "value"):
                self._activeExtruder.setProperty(property, "value", self._extruder_cache[property])
                #self._activeExtruder.setProperty(property, "state", InstanceState.Default)

        for prop in self._propertiesChanged:
            if prop is SmartSliceValidationProperty.MaxDisplacement:
                self.connector._proxy.setMaximalDisplacement()
            elif prop is SmartSliceValidationProperty.FactorOfSafety:
                self.connector._proxy.setFactorOfSafety()
            elif prop is SmartSliceValidationProperty.LoadDirection:
                #print ("Load Direction Stats:  " + str(self.connector._proxy._loadDirection) +", " + str(self.connector._proxy.reqsLoadDirection))
                self.connector._proxy.setLoadDirection()
            elif prop is SmartSliceValidationProperty.LoadMagnitude:
                self.connector._proxy.setLoadMagnitude()

            #  Face Selection
            elif prop is SmartSliceValidationProperty.SelectedFace:
                self.selectedFacesChanged.emit()

            #  Material
            elif prop is SmartSliceValidationProperty.Material:
                self.setMaterial()
                #self._propertiesChanged.pop()
            elif prop is SmartSliceValidationProperty.MeshScale:
                self.setMeshScale
                self._newScale = self.meshScale
                #self._propertiesChanged.pop()
            elif prop is SmartSliceValidationProperty.MeshRotation:
                self.setMeshRotation
                self._newRotation = self.meshRotation
            


        
        #print ("\nTest Property Cache:  " + str(self._activeExtruder.getProperty("infill_sparse_density", "value")) + "\n")

    def prepareCache(self):
        self.clearChangedProperties()
        self.connector._proxy.confirmationWindowEnabled = False
        self.connector._proxy.confirmationWindowEnabledChanged.emit()

    cacheRestored = Signal()

    #
    #   CONFIRM/CANCEL PROPERTY CHANGES
    #

    def _onConfirmRequirements(self):
        i = 0
        for prop in self._propertiesChanged:
            if prop is SmartSliceValidationProperty.MaxDisplacement:
                self.connector._proxy.reqsMaxDeflect = self._changedValues.pop(i)
                self.connector._proxy.setMaximalDisplacement()
                self._propertiesChanged.pop(i)
            elif prop is SmartSliceValidationProperty.FactorOfSafety:
                self.connector._proxy.reqsSafetyFactor = self._changedValues.pop(i)
                self.connector._proxy.setFactorOfSafety()
                self._propertiesChanged.pop(i)
            i += 1


    def _onConfirmChanges(self):
        self.cacheChanges()
        self.connector.ConfirmationConcluded.emit()

    def _onCancelChanges(self):

        self._cancellingChanges.acquire()

        try:
            print ("Cancelling Change!!!")
            self._cancellingChanges._locked = True
            self._cancelChanges = True
            self.restoreCache()
            print ("Change Cancelled!!!")

        finally:
            self.connector.ConfirmationConcluded.emit()
            if self._cancellingChanges.locked():
                self._cancellingChanges.release()
            print("Finished Restoring")


    def getGlobalProperty(self, key):
        return self._global_cache[key]

    def getExtruderProperty(self, key):
        return self._extruder_cache[key]

    #
    #  LOCAL TRANSFORMATION PROPERTIES
    #

    def connectMeshSignals(self, unused):
        i = 0
        _root = self._sceneRoot 

        for node in _root.getAllChildren():
            print ("Node Found:  " + node.getName())
            if node.getName() == "3d":
                if (self._sceneNode is None) or (self._sceneNode.getName() != _root.getAllChildren()[i+1].getName()):
                    if self._sceneNode is not None:
                        self._sceneNode.transformationChanged.disconnectAll()

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


    #
    #  LOCAL TRANSFORMATION
    #

    def _onLocalTransformationChanged(self, node):
        if node.getScale() != self.meshScale:
            self.onMeshScaleChanged()
        if node.getOrientation() != self.meshRotation:
            self.onMeshRotationChanged()

    def setMeshScale(self):
        #print ("\nMesh Scale Set\n")
        self._sceneNode.setScale(self.meshScale)
        self._sceneNode.transformationChanged.emit(self._sceneNode)

    def onMeshScaleChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing) or (self.connector.status is SmartSliceCloudStatus.Optimized):
            self._propertiesChanged.append(SmartSliceValidationProperty.MeshScale)
            self._changedValues.append(0)
            self._newScale = self._sceneNode.getScale()
            #print ("Mesh Scale Change Confirmed")
            self.connector._proxy.shouldRaiseWarning = True
            self.connector.confirmValidation.emit()
        else:
            #print ("\nMesh Scale Set\n")
            self.meshScale = self._sceneNode.getScale()
            self.connector._prepareValidation()

    def setMeshRotation(self):
        #print ("\nMesh Rotation Set\n")
        self._sceneNode.setOrientation(self.meshRotation)
        self._sceneNode.transformationChanged.emit(self._sceneNode)

    def onMeshRotationChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing) or (self.connector.status is SmartSliceCloudStatus.Optimized):
            self._propertiesChanged.append(SmartSliceValidationProperty.MeshRotation)
            self._changedValues.append(0)
            self._newRotation = self._sceneNode.getOrientation()
            self.connector._proxy.shouldRaiseWarning = True
            self.connector.confirmValidation.emit()
        else:
            self.meshRotation = self._sceneNode.getOrientation()
            self.connector._prepareValidation()



    #
    #   MATERIAL CHANGES
    #
    activeMaterialChanged = Signal()

    def setMaterial(self):
       self._activeExtruder.material = self._material
       

    def _onMaterialChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing) or (self.connector.status is SmartSliceCloudStatus.Optimized):
            #print("\n\nMATERIAL CHANGE CONFIRMED HERE\n\n")
            #if len(self._propertiesChanged) > 1:
            if self._material is not self._activeExtruder.material:
                self._propertiesChanged.append(SmartSliceValidationProperty.Material)
                self._changedValues.append(self._activeExtruder.material)
                self.connector.confirmValidation.emit()
        else:
            #print("\n\nMATERIAL CHANGED HERE\n\n")
            #  TODO:  Next line is commented because there are two signals that are thrown
            #self.connector._prepareValidation()
            self._material = self._activeExtruder.material
            
    #
    #   FACE SELECTION
    #

    selectedFacesChanged = Signal() 

    def confirmFaceDraw(self, force=None):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing) or (self.connector.status is SmartSliceCloudStatus.Optimized):
            self._propertiesChanged.append(SmartSliceValidationProperty.SelectedFace)
            self.connector.confirmValidation.emit()
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

        print ("Checking Property:  " + key)

        if self._cancellingChanges.locked():
            return

        else:
            if key not in self.global_keys:
                print (str(key) + "\n")
                return
            if self._globalStack.getProperty(key, property_name) == self._global_cache[key]:
                return

            if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing) or (self.connector.status is SmartSliceCloudStatus.Optimized):
                self.connector.confirmValidation.emit()
            else:
                self.connector._prepareValidation()
                self._global_cache[key] = self._globalStack.getProperty(key, "value")


    # On EXTRUDER Property Changed
    def _onExtruderPropertyChanged(self, key: str, property_name: str):

        if self._cancellingChanges.locked():
            print ("LOCKED OUT!!!")
            return
        
        else:
            if key not in self.extruder_keys:
                return
            elif self._activeExtruder.getProperty(key, property_name) == self._extruder_cache[key]:
                return

            elif not self._cancelChanges:        
                print ("Checking Property:  " + key)
                if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing) or (self.connector.status is SmartSliceCloudStatus.Optimized):
                    #  Confirm Settings Changes
                    self.connector.confirmValidation.emit()
                else:
                    self.connector._prepareValidation()
                    self._extruder_cache[key] = self._activeExtruder.getProperty(key, "value")
        