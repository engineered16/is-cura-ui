#   SmartSlicePropertyHandler.py
#   Teton Simulation
#   Authored on   January 3, 2019
#   Last Modified January 3, 2019

#
#  Contains procedures for handling Cura Properties in accordance with SmartSlice
#

import copy
import time, threading
from copy import copy

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
from UM.Math.Vector import Vector

#  Smart Slice
from .SmartSliceCloudProxy import SmartSliceCloudStatus
from .SmartSliceProperty import SmartSliceProperty, SmartSliceLoadDirection, SmartSliceContainerProperties

"""
  SmartSlicePropertyHandler(connector)
    connector: CloudConnector, used for interacting with rest of SmartSlice plugin

    The Property Handler contains functionality for manipulating all settings that
      affect Smart Slice validation/optimization results.  
    It manages a cache of properties including Global/Extruder container properties 
      retrieved from Cura's backend, as well as SmartSlice settings (e.g. Load/Anchor)
"""
class SmartSlicePropertyHandler(QObject):
    def __init__(self, connector):
        super().__init__()

        #  Callback
        self.connector = connector
        self._confirming = False
        self._initialized = False
        
        #  General Purpose Cache Space
        self._propertiesChanged = []
        self._changedValues     = []
        self._hasChanges = False
        self._global_cache = {}
        self._extruder_cache = {}
        #  General Purpose properties which affect Smart Slice
        self._container_properties = SmartSliceContainerProperties()

        #  Mesh Properties
        self.meshScale = None
        self._newScale = None
        self.meshRotation = None
        self._newRotation = None
        #  Scene (for mesh/transform signals)
        self._sceneNode = None
        self._sceneRoot = Application.getInstance().getController().getScene().getRoot()

        #  Selection Proeprties
        self._selection_mode = 1 # Default to AnchorMode
        self._changedMesh = None
        self._changedFaces = None
        self._changedForce = None
        self._anchoredMesh = None
        self._anchoredFaces = None
        self._anchoredID = None
        self._loadedMesh = None
        self._loadedFaces = None
        self._loadedID = None
        
        #  Cura Setup
        self._activeMachineManager = CuraApplication.getInstance().getMachineManager()
        self._globalStack = self._activeMachineManager.activeMachine
        
        #  Check that a printer has been set-up by the wizard.
        #  TODO:  Add a signal listener for when Machine is added
        if self._globalStack is not None:
            self._onMachineChanged()

        #  Cancellation Variable
        self._cancelChanges = False

        #  Temporary Cache
        self._cachedScene = None
        self._cachedFaceID = None
        self._cachedTriangles = None


    #
    #   CACHE HANDLING
    #

    #  Refresh Cache State
    """
      clearChangedProperties()
        Clear all pending changed properties/values
    """
    def clearChangedProperties(self):
        self._propertiesChanged = []
        self._changedValues = []
            
    """
      prepareCache()
        Clears any pending changes to cache and silences confirmation prompt
    """
    def prepareCache(self):
        self.clearChangedProperties()
        self.connector._proxy.confirmationWindowEnabled = False
        self.connector._proxy.confirmationWindowEnabledChanged.emit()

    #  Cache Changes
    """
      cacheChanges()
        Stores all current values in Cura environment to SmartSlice cache
    """
    def cacheChanges(self):
        self.cacheSmartSlice()
        self.cacheGlobal()
        self.cacheExtruder()

    """
      cacheGlobal()
        Caches properties that are used throughout Cura's Global Environment
    """
    def cacheGlobal(self):
        self._global_cache = {}

        for key in self._container_properties.global_keys:
            if key not in self._global_cache:
                self._global_cache[key] = self._globalStack.getProperty(key, "value")
            if self._global_cache[key] != self._globalStack.getProperty(key, "value"):
                self._global_cache[key] = self._globalStack.getProperty(key, "value")
            
    """
      cacheExtruder()
        Caches properties that are used for the active extruder
    """
    def cacheExtruder(self):
        self._extruder_cache = {}

        for key in self._container_properties.extruder_keys:
            if key not in self._extruder_cache:
                self._extruder_cache[key] = self._activeExtruder.getProperty(key, "value")
            if self._extruder_cache[key] != self._activeExtruder.getProperty(key, "value"):
                self._extruder_cache[key] = self._activeExtruder.getProperty(key, "value")

    """
      cacheSmartSlice()
        Caches properties that are only used in SmartSlice Environment
    """
    def cacheSmartSlice(self):
        i = 0
        for prop in self._propertiesChanged:
            if prop is SmartSliceProperty.MaxDisplacement:
                self.connector._proxy.reqsMaxDeflect = self._changedValues[i]
                self.connector._proxy.setMaximalDisplacement()
            elif prop is SmartSliceProperty.FactorOfSafety:
                self.connector._proxy.reqsSafetyFactor = self._changedValues[i]
                self.connector._proxy.setFactorOfSafety()
            elif prop is SmartSliceProperty.LoadDirection:
                self.connector._proxy.reqsLoadDirection = self._changedValues[i]
                self.connector._proxy.setLoadDirection()
            elif prop is SmartSliceProperty.LoadMagnitude:
                self.connector._proxy.reqsLoadMagnitude = self._changedValues[i]
                self.connector._proxy.setLoadMagnitude()

          #  Face Selection
            elif prop is SmartSliceProperty.SelectedFace:
                self.updateMeshes()
                self.selectedFacesChanged.emit()

          #  Material
            elif prop is SmartSliceProperty.Material:
                self._material = self._changedValues[i]
                self.setMaterial()
                self._propertiesChanged.pop()
            elif prop is SmartSliceProperty.MeshScale:
                self.meshScale = self._newScale
                self.setMeshScale()
                self._newScale = self.meshScale
                self._propertiesChanged.pop()
            elif prop is SmartSliceProperty.MeshRotation:
                self.meshRotation = self._newRotation
                self.setMeshRotation()
                self._newRotation = self.meshRotation
                self._propertiesChanged.pop()
            i += 0
        self.clearChangedProperties()

        if self._cachedFaceID is not None:
            self.applyAnchorOrLoad(self._cachedTriangles)
            self._cachedFaceID = None

    #  Restore Properties from Cache
    cacheRestored = Signal()

    """
      restoreCache()
        Restores all cached values for properties upon user cancellation
    """
    def restoreCache(self):
        for property in self._global_cache:
            if self._global_cache[property] != self._globalStack.getProperty(property, "value"):
                self._lastCancel = property
                self._globalStack.setProperty(property, "value", self._global_cache[property])
                #self._globalStack.setProperty(property, "state", InstanceState.Default)

        for property in self._extruder_cache:
            if self._extruder_cache[property] != self._activeExtruder.getProperty(property, "value"):
                self._lastCancel = property
                self._activeExtruder.setProperty(property, "value", self._extruder_cache[property])
                #self._activeExtruder.setProperty(property, "state", InstanceState.Default)

        for prop in self._propertiesChanged:
            self._lastCancel = prop
            if prop is SmartSliceProperty.MaxDisplacement:
                self.connector._proxy.setMaximalDisplacement()
            elif prop is SmartSliceProperty.FactorOfSafety:
                self.connector._proxy.setFactorOfSafety()
            elif prop is SmartSliceProperty.LoadDirection:
                self.connector._proxy.setLoadDirection()
            elif prop is SmartSliceProperty.LoadMagnitude:
                self.connector._proxy.setLoadMagnitude()

            #  Face Selection
            elif prop is SmartSliceProperty.SelectedFace:
                self.selectedFacesChanged.emit()

            #  Material
            elif prop is SmartSliceProperty.Material:
                self.setMaterial()
                #self._propertiesChanged.pop()
            elif prop is SmartSliceProperty.MeshScale:
                self.setMeshScale
                self._newScale = self.meshScale
                #self._propertiesChanged.pop()
            elif prop is SmartSliceProperty.MeshRotation:
                self.setMeshRotation
                self._newRotation = self.meshRotation


    #
    #   CONFIRM/CANCEL PROPERTY CHANGES
    #

    def _onConfirmRequirements(self):
        i = 0
        for prop in self._propertiesChanged:
            if prop is SmartSliceProperty.MaxDisplacement:
                self.connector._proxy.reqsMaxDeflect = self._changedValues.pop(i)
                self.connector._proxy.setMaximalDisplacement()
                self._propertiesChanged.pop(i)
            elif prop is SmartSliceProperty.FactorOfSafety:
                self.connector._proxy.reqsSafetyFactor = self._changedValues.pop(i)
                self.connector._proxy.setFactorOfSafety()
                self._propertiesChanged.pop(i)
            i += 1

    def _onConfirmChanges(self):
        self.cacheChanges()
        self.connector.confirmationConcluded.emit()

    def _onCancelChanges(self):
        Logger.log ("d", "Cancelling Change in Smart Slice Environment")
        self._cancelChanges = True
        x = threading.Thread(target=self.resetCancelCheck)
        x.start()
        self.restoreCache()
        self.connector.confirmationConcluded.emit()
        Logger.log ("d", "Cancelled Change in Smart Slice Environment")

    """
      resetCancelCheck()
        Silences second 'Confirm Changes' prompt after a user cancels
    """ 
    def resetCancelCheck(self):
        #  NOTE: Increase delay if a setting change 
        #         erroneously raises a second confirmation prompt 
        time.sleep(0.35)
        self._cancelChanges = False


    #
    #   CURA PROPERTY ACCESSORS
    #

    """
      getGlobalProperty(key)
        key: String 'key' value for referencing global property value
    """
    def getGlobalProperty(self, key):
        return self._global_cache[key]

    """
      getExtruderProperty(key)
        key: String 'key' value for referencing active extruder property value
    """
    def getExtruderProperty(self, key):
        return self._extruder_cache[key]


    #
    #  LOCAL TRANSFORMATION PROPERTIES
    #

    """
      connectMeshSignals()
        When a mesh is loaded, this method is called to connect signals for detecting mesh transform changes
    """
    def connectMeshSignals(self, unused=None):
        i = 0
        _root = self._sceneRoot 

        for node in _root.getAllChildren():
            if node.getName() == "3d":
                if (self._sceneNode is None) or (self._sceneNode.getName() != _root.getAllChildren()[i+1].getName()):
                    if self._sceneNode is not None:
                        self._sceneNode.transformationChanged.disconnectAll()

                    self._sceneNode = _root.getAllChildren()[i+1]
                    Logger.log ("d", "\nFile Found:  " + self._sceneNode.getName() + "\n")

                    #  Set Initial Scale/Rotation
                    self.meshScale    = self._sceneNode.getScale()
                    self.meshRotation = self._sceneNode.getOrientation()

                    #  TODO: Properly Disconnect this Signal, when figure out where to do so
                    self._sceneNode.transformationChanged.connect(self._onLocalTransformationChanged)
                    i += 1
            i += 1
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
        self._sceneNode.setScale(self.meshScale)
        self._sceneNode.transformationChanged.emit(self._sceneNode)

    def onMeshScaleChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing) or (self.connector.status is SmartSliceCloudStatus.Optimized):
            self._propertiesChanged.append(SmartSliceProperty.MeshScale)
            self._changedValues.append(0)
            self._newScale = self._sceneNode.getScale()
            self.connector._proxy.shouldRaiseWarning = True
            self.connector.confirmValidation.emit()
        else:
            self.meshScale = self._sceneNode.getScale()
            self.connector._prepareValidation()

    def setMeshRotation(self):
        self._sceneNode.setOrientation(self.meshRotation)
        self._sceneNode.transformationChanged.emit(self._sceneNode)

    def onMeshRotationChanged(self):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing) or (self.connector.status is SmartSliceCloudStatus.Optimized):
            self._propertiesChanged.append(SmartSliceProperty.MeshRotation)
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
                self._propertiesChanged.append(SmartSliceProperty.Material)
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

    def applyAnchorOrLoad(self, selected_triangles):
        if self._selection_mode is 1:
            self.connector.resetAnchor0FacesPoc()
            self.connector.appendAnchor0FacesPoc(selected_triangles)
            Logger.log("d", "cloud_connector.getAnchor0FacesPoc(): {}".format(self.connector.getAnchor0FacesPoc()))
        else: 

            load_vector = selected_triangles[0].normal

            self.connector.updateForce0Vector(
                Vector(load_vector.r, load_vector.s, load_vector.t)
            )

            self.connector.resetForce0FacesPoc()
            self.connector.appendForce0FacesPoc(selected_triangles)

            Logger.log("d", "cloud_connector.getForce0VectorPoc(): {}".format(self.connector.getForce0VectorPoc()))
            Logger.log("d", "cloud_connector.getForce0FacesPoc(): {}".format(self.connector.getForce0FacesPoc()))


        

    def drawAnchorOrLoad(self, scene_node, face_id, selected_triangles):

        if self._selection_mode is 1: #  Anchor

            #  Set/Draw Anchor Selection in Scene
            self.connector._proxy._anchorsApplied = 1
            self._anchoredID = face_id
        else:   # Load

            #  Set/Draw Scene Properties
            self.connector._proxy._loadsApplied = 1
            self._loadedID = face_id

    def confirmFaceDraw(self, scene_node=None, face_id=None, selected_triangles=None):
        if self.connector.status is SmartSliceCloudStatus.BusyValidating or (self.connector.status is SmartSliceCloudStatus.BusyOptimizing) or (self.connector.status is SmartSliceCloudStatus.Optimized):
            self._propertiesChanged.append(SmartSliceProperty.SelectedFace)
            self._cachedScene = scene_node
            self._cachedTriangles = selected_triangles
            self._cachedFaceID = face_id
            if self._selection_mode is 1:
                if self._anchoredID is not face_id:
                    self.connector.confirmValidation.emit()
            else:
                if self._loadedID is not face_id:
                    self.connector.confirmValidation.emit()
        else:
            if self._selection_mode is 1:
                if self._anchoredID is not None and (self._anchoredID is face_id):
                    self.updateMeshes()
                    return
            else:
                if self._loadedID is not None and (self._loadedID is face_id):
                    self.updateMeshes()
                    return
            self.connector._prepareValidation()
            self.updateMeshes()
            self.drawAnchorOrLoad(scene_node, face_id, selected_triangles)
            self.applyAnchorOrLoad(selected_triangles)
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
    #   CURA PROPERTY SIGNAL LISTENERS
    #

    # On GLOBAL Property Changed
    def _onGlobalPropertyChanged(self, key: str, property_name: str):

        if key not in self._container_properties.global_keys:
            return
        if self._globalStack.getProperty(key, property_name) == self._global_cache[key]:
            return

        if self.connector.status in {SmartSliceCloudStatus.BusyValidating, SmartSliceCloudStatus.BusyOptimizing, SmartSliceCloudStatus.Optimized}:
            self.connector.confirmValidation.emit()
        else:
            self.connector._prepareValidation()
            self._global_cache[key] = self._globalStack.getProperty(key, "value")

    # On EXTRUDER Property Changed
    def _onExtruderPropertyChanged(self, key: str, property_name: str):

        if key not in self._container_properties.extruder_keys:
            return
        elif self._activeExtruder.getProperty(key, property_name) == self._extruder_cache[key]:
            return

        if self.connector.status in {SmartSliceCloudStatus.BusyValidating, SmartSliceCloudStatus.BusyOptimizing, SmartSliceCloudStatus.Optimized}:
            #  Confirm Settings Changes
            if not self.connector._proxy.confirmationWindowEnabled:
                self.connector.confirmValidation.emit()
        else:
            self.connector._prepareValidation()
            self._extruder_cache[key] = self._activeExtruder.getProperty(key, "value")


    #  Configure Extruder/Machine Settings for Smart Slice
    def _onMachineChanged(self):
        self._activeExtruder = self._globalStack.extruderList[0]

        self._material = self._activeMachineManager._global_container_stack.extruderList[0].material #  Cura Material Node

        #  Connect Signals
        self._globalStack.propertyChanged.connect(self._onGlobalPropertyChanged)            #  Global
        self._activeExtruder.propertyChanged.connect(self._onExtruderPropertyChanged)       #  Extruder
        self._activeMachineManager.activeMaterialChanged.connect(self._onMaterialChanged)   #  Material
        self._sceneRoot.childrenChanged.connect(self.connectMeshSignals)                    #  Mesh Transform
