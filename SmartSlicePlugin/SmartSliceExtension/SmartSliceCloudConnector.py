'''
Created on 22.10.2019

@author: thopiekar
'''

import time
import os
import tempfile
import json
import zipfile

import pywim

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QTime
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkReply
from PyQt5.QtNetwork import QNetworkRequest
from PyQt5.QtNetwork import QNetworkAccessManager
from PyQt5.QtQml import qmlRegisterSingletonType

from UM.Application import Application
from UM.Job import Job
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry
from UM.Scene.Iterator.DepthFirstIterator import DepthFirstIterator

from .SmartSliceCloudProxy import SmartSliceCloudStatus
from .SmartSliceCloudProxy import SmartSliceCloudProxy

## Draft of an connection check
class ConnectivityChecker(QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url = QUrl("https://amazonaws.com/")
        req = QNetworkRequest(url)
        self.net_manager = QNetworkAccessManager()
        self.res = self.net_manager.get(req)
        self.res.finished.connect(self.processRes)
        self.res.error.connect(self.processErr)

    @pyqtSlot()
    def processRes(self):
        if self.res.bytesAvailable():
            # Success
            pass
        self.res.deleteLater()

    @pyqtSlot(QNetworkReply.NetworkError)
    def processErr(self, code):
        print(code)

class SmartSliceCloudVerificationJob(Job):
    # This job is responsible for uploading the backup file to cloud storage.
    # As it can take longer than some other tasks, we schedule this using a Cura Job.
    def __init__(self, connector) -> None:
        super().__init__()
        self.connector = connector

    def run(self) -> None:
        # TODO: Add instructions how to send a verification job here
        time.sleep(5)
        if not self.connector._demo_was_underdimensioned_before:
            self.connector.status = SmartSliceCloudStatus.Underdimensioned
            self.connector._demo_was_underdimensioned_before = True
            
            self.connector._proxy.resultSafetyFactor = 0.5
            self.connector._proxy.resultMaximalDisplacement = 5
            
            self.connector._proxy.resultTimeInfill = QTime(1, 0, 0, 0)
            self.connector._proxy.resultTimeInnerWalls = QTime(0, 20, 0, 0)
            self.connector._proxy.resultTimeOuterWalls = QTime(0, 15, 0, 0)
            self.connector._proxy.resultTimeRetractions = QTime(0, 5, 0, 0)
            self.connector._proxy.resultTimeSkin = QTime(0, 10, 0, 0)
            self.connector._proxy.resultTimeSkirt = QTime(0, 1, 0, 0)
            self.connector._proxy.resultTimeTravel = QTime(0, 30, 0, 0)
        
        elif not self.connector._demo_was_overdimensioned_before:
            self.connector.status = SmartSliceCloudStatus.Overdimensioned
            self.connector._demo_was_overdimensioned_before = True
            
            self.connector._proxy.resultSafetyFactor = 2
            self.connector._proxy.resultMaximalDisplacement = 1
            
            self.connector._proxy.resultTimeInfill = QTime(2, 0, 0, 0)
            self.connector._proxy.resultTimeInnerWalls = QTime(0, 10, 0, 0)
            self.connector._proxy.resultTimeOuterWalls = QTime(0, 20, 0, 0)
            self.connector._proxy.resultTimeRetractions = QTime(0, 3, 0, 0)
            self.connector._proxy.resultTimeSkin = QTime(0, 15, 0, 0)
            self.connector._proxy.resultTimeSkirt = QTime(0, 2, 0, 0)
            self.connector._proxy.resultTimeTravel = QTime(0, 45, 0, 0)
        else:
            self.connector.status = SmartSliceCloudStatus.Optimized
            
            self.connector._proxy.resultSafetyFactor = 1
            self.connector._proxy.resultMaximalDisplacement = 2
            
            self.connector._proxy.resultTimeInfill = QTime(3, 0, 0, 0)
            self.connector._proxy.resultTimeInnerWalls = QTime(0, 10, 0, 0)
            self.connector._proxy.resultTimeOuterWalls = QTime(0, 20, 0, 0)
            self.connector._proxy.resultTimeRetractions = QTime(0, 3, 0, 0)
            self.connector._proxy.resultTimeSkin = QTime(0, 15, 0, 0)
            self.connector._proxy.resultTimeSkirt = QTime(0, 2, 0, 0)
            self.connector._proxy.resultTimeTravel = QTime(0, 45, 0, 0)

SmartSliceCloudOptimizeJob = SmartSliceCloudVerificationJob

class SmartSliceCloudConnector(QObject):
    token_preference = "smartslice/token"
    
    def __init__(self, extension):
        super().__init__()
        self.extension = extension
        
        # DEMO variables
        self._demo_was_underdimensioned_before = False
        self._demo_was_overdimensioned_before = False
        
        # Variables 
        self._status = None
        self._job = None
        
        # Proxy
        self._proxy = SmartSliceCloudProxy(self)
        self._proxy.sliceButtonClicked.connect(self.onSliceButtonClicked)
        
        # Connecting signals
        self.doVerification.connect(self._doVerfication)
        self.doOptimization.connect(self._doOptimization)
        
        # Application stuff
        Application.getInstance().getPreferences().addPreference(self.token_preference, "")
        Application.getInstance().activityChanged.connect(self._onApplicationActivityChanged)

    def getProxy(self, engine, script_engine):
        return self._proxy

    def _onEngineCreated(self):
        qmlRegisterSingletonType(SmartSliceCloudProxy,
                                 "SmartSlice",
                                 1, 0,
                                 "Cloud",
                                 self.getProxy
                                 )
        
        self.status = SmartSliceCloudStatus.InvalidInput

    def updateSliceWidget(self):
        if self.status is SmartSliceCloudStatus.InvalidInput:
            self._proxy.sliceStatus = "Amount of loaded models is incorrect"
            self._proxy.sliceHint = "Make sure only one model is loaded!"
            self._proxy.sliceButtonText = "Waiting for model"
            self._proxy.sliceButtonEnabled = False
        elif self.status is SmartSliceCloudStatus.ReadyToVerify:
            self._proxy.sliceStatus = "Ready to verify"
            self._proxy.sliceHint = "Press on the button below to verify your part."
            self._proxy.sliceButtonText = "Verify"
            self._proxy.sliceButtonEnabled = True
        elif self.status is SmartSliceCloudStatus.BusyValidating:
            self._proxy.sliceStatus = "Verifying your part"
            self._proxy.sliceHint = "Please wait until the verification is done."
            self._proxy.sliceButtonText = "Busy..."
            self._proxy.sliceButtonEnabled = False
        elif self.status is SmartSliceCloudStatus.Underdimensioned:
            self._proxy.sliceStatus = "Your part is underdimensioned!"
            self._proxy.sliceHint = "Press the button below to strengthen your part."
            self._proxy.sliceButtonText = "Optimize"
            self._proxy.sliceButtonEnabled = True
        elif self.status is SmartSliceCloudStatus.Overdimensioned:
            self._proxy.sliceStatus = "Your part is overdimensioned!"
            self._proxy.sliceHint = "Press the button to reduce needed material."
            self._proxy.sliceButtonText = "Optimize"
            self._proxy.sliceButtonEnabled = True
        elif self.status is SmartSliceCloudStatus.BusyOptimizing:
            self._proxy.sliceStatus = "Optimizing your part"
            self._proxy.sliceHint = "Please wait until the optimization is done."
            self._proxy.sliceButtonText = "Busy..."
            self._proxy.sliceButtonEnabled = False
        elif self.status is SmartSliceCloudStatus.Optimized:
            self._proxy.sliceStatus = "Part optimized"
            self._proxy.sliceHint = "Well done! Now your part suites your needs!"
            self._proxy.sliceButtonText = "Done"
            self._proxy.sliceButtonEnabled = False
        else:
            self._proxy.sliceStatus = "! INTERNAL ERRROR!"
            self._proxy.sliceHint = "! UNKNOWN STATUS ENUM SET!"
            self._proxy.sliceButtonText = "! FOOO !"
            self._proxy.sliceButtonEnabled = False
    
        # Setting icon path
        stage_path = PluginRegistry.getInstance().getPluginPath("SmartSliceStage")
        stage_images_path = os.path.join(stage_path, "images")
        icon_done_green = os.path.join(stage_images_path, "done_green.svg")
        icon_error_red = os.path.join(stage_images_path, "error_red.svg")
        icon_warning_yellow = os.path.join(stage_images_path, "warning_yellow.svg")
        current_icon = icon_done_green
        if self.status is SmartSliceCloudStatus.Overdimensioned:
            current_icon = icon_warning_yellow
        elif self.status is SmartSliceCloudStatus.Underdimensioned:
            current_icon = icon_error_red
        self._proxy.sliceIconImage = current_icon
        
        # Setting icon visibiltiy
        if self.status is SmartSliceCloudStatus.Optimized or self.status in SmartSliceCloudStatus.Optimizable:
            self._proxy.sliceIconVisible = True
        else:
            self._proxy.sliceIconVisible = False

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if self._status is not value:
            self._status = value
            
            self.updateSliceWidget()
    
    @property
    def token(self):
        return Application.getInstance().getPreferences().getValue(self.token_preference)
    
    @token.setter
    def token(self, value):
        Application.getInstance().getPreferences().setValue(self.token_preference, value)
    
    def login(self):
        #username = self._proxy.loginName()
        #password = self._proxy.loginPassword()
        
        if True:
            self.token = "123456789qwertz"
            return True
        else:
            self.token = ""
            return False

    def getSliceableNodes(self):
        scene_node = Application.getInstance().getController().getScene().getRoot()
        sliceable_nodes = []

        for node in DepthFirstIterator(scene_node):
            if node.callDecoration("isSliceable"):
                sliceable_nodes.append(node)

        return sliceable_nodes

    def _onApplicationActivityChanged(self):
        slicable_nodes_count = len(self.getSliceableNodes())
        
        # TODO: Add check for anchors and loads here!
        
        if slicable_nodes_count == 1:
            self.status = SmartSliceCloudStatus.ReadyToVerify
        else:
            self.status = SmartSliceCloudStatus.InvalidInput
    
    def _onJobFinished(self, job):
        self._job = None
    
    doVerification = pyqtSignal()
    
    def _doVerfication(self):
        self._job = SmartSliceCloudVerificationJob(self)
        self._job.finished.connect(self._onJobFinished)
        self._job.start()
    
    doOptimization = pyqtSignal()
    
    def _doOptimization(self):
        self._job = SmartSliceCloudOptimizeJob(self)
        self._job.finished.connect(self._onJobFinished)
        self._job.start()
    
    def onSliceButtonClicked(self):
        if self.status is SmartSliceCloudStatus.ReadyToVerify:
            self.status = SmartSliceCloudStatus.BusyValidating
            self.doVerification.emit()
        elif self.status in SmartSliceCloudStatus.Optimizable:
            self.status = SmartSliceCloudStatus.BusyOptimizing
            self.doOptimization.emit()

    @property
    def variables(self):
        return self.extension.getVariables(None, None)

    def prepareInitial3mf(self, location=None):
        # Using tempfile module to probe for a temporary file path
        # TODO: We can do this more elegant of course, too.
        if not location:
            file = tempfile.NamedTemporaryFile(suffix=".3mf")
            location = file.name
            del(file)
            Logger.log("d", "location: {}".format(location))

        # Checking whether count of models == 1
        mesh_nodes = self.getSliceableNodes()
        if len(mesh_nodes) is not 1:
            Logger.log("d", "Found {} meshes!".format(["no", "too many"][len(mesh_nodes) > 1]))
            return None

        # Getting 3MF writer and write our file
        threeMF_Writer = PluginRegistry.getInstance().getPluginObject("3MFWriter")
        threeMF_Writer.write(location, mesh_nodes)

        return location

    def appendTo3mf(self, filename, node):
        machine_manager = Application.getInstance().getMachineManager()
        active_machine = machine_manager.activeMachine
        
        active_extruder = node.callDecoration("getActiveExtruderPosition")
        
        extruders = list(active_machine.extruders.values())
        extruders = sorted(extruders, key = lambda extruder: extruder.getMetaDataEntry("position"))

        material_guids_per_extruder = [extruder.material.getMetaData().get("GUID", "") for extruder in extruders]

        # TODO: Needs to be determined from the used model
        guid = material_guids_per_extruder[active_extruder]
        
        # Determine material properties from material database
        this_dir = os.path.split(__file__)[0]
        database_location = os.path.join(this_dir, "data", "POC_material_database.json")
        jdata = json.loads(open(database_location).read())
        material_found = None
        for material in jdata["materials"]:
            if "cura-guid" not in material.keys():
                continue
            if guid in material["cura-guid"]:
                material_found = material
                break
        
        if not material_found:
            return None
        
        job = pywim.smartslice.job.Job()

        job.type = pywim.smartslice.job.JobType.optimization
    
        # Create the bulk material definition. This likely will be pre-defined
        # in a materials database or file somewhere
        job.bulk = pywim.fea.model.Material(name=material_found["name"])
        job.bulk.density = material_found["density"]
        job.bulk.elastic = pywim.fea.model.Elastic(properties={'E': material_found['E'],
                                                               'nu': material_found['v']})
    
        # Setup optimization configuration
        job.optimization.min_safety_factor = self.variables.safetyFactor
        job.optimization.max_displacement = self.variables.maxDeflect
    
        # Setup the chop model - chop is responsible for creating an FEA model
        # from the triangulated surface mesh, slicer configuration, and
        # the prescribed boundary conditions
        
        # The chop.model.Model class has an attribute for defining
        # the mesh, however, it's not necessary that we do so.
        # When the back-end reads the 3MF it will obtain the mesh
        # from the 3MF object model, therefore, defining it in the 
        # chop object would be redundant.
        #job.chop.meshes.append( ... ) <-- Not necessary
    
        # Define the load step for the FE analysis
        step = pywim.chop.model.Step(name='default')
    
        # Create the fixed boundary conditions (anchor points)
        anchor1 = pywim.chop.model.FixedBoundaryCondition(name='anchor1')
    
        # Add the face Ids from the STL mesh that the user selected for
        # this anchor
        anchor1.face.extend(
            (97, 98, 111, 112)
        )
    
        step.boundary_conditions.append(anchor1)
    
        # Add any other boundary conditions in a similar manner...
    
        # Create an applied force
        force1 = pywim.chop.model.Force(name='force1')
    
        # Set the components on the force vector. In this example
        # we have 100 N, 200 N, and 50 N in the x, y, and z
        # directions respectfully.
        force1.force.set((100., 200., 50.))
    
        # Add the face Ids from the STL mesh that the user selected for
        # this force
        force1.face.extend(
            (156, 157, 158)
        )
    
        step.loads.append(force1)
    
        # Add any other loads in a similar manner...
    
        # Append the step definition to the chop model. Smart Slice only
        # supports one step right now. In the future we may allow multiple
        # loading steps.
        job.chop.steps.append(step)
    
        # Now we need to setup the print/slicer configuration
        
        print_config = pywim.am.Config()
        print_config.layer_width = 0.45
        # ... and so on, check pywim.am.Config for full definition
    
        # The am.Config contains an "auxiliary" dictionary which should
        # be used to define the slicer specific settings. These will be
        # passed on directly to the slicer (CuraEngine).
        print_config.auxiliary['print_bed_temperature'] = '60.0'
    
        # Setup the slicer configuration. See each class for more
        # information.
        extruder0 = pywim.chop.machine.Extruder(diameter=0.4)
        printer = pywim.chop.machine.Printer(name=active_machine.getName(), extruders=(extruder0, ))
    
        # And finally set the slicer to the Cura Engine with the config and printer defined above
        job.chop.slicer = pywim.chop.slicer.CuraEngine(config=print_config, printer=printer)
    
        with zipfile.ZipFile(filename, 'a') as tmf:
            tmf.writestr('SmartSlice/job.json', job.to_json())
        

        return filename

    def sendJob(self):
        Logger.log("d", "Sending slice job!")
        filename = self.prepareInitial3mf()

        if not filename:
            return None

        self.appendTo3mf(filename)

        # SEND YOUR 3MF TO THE CLOUD HERE

        # PROCESS THE DIRECT RESPONSE AND/OR WAIT

        # EMITTING A SIGNAL WITH THE RESULTS AND DISPLAY THEM IN QML
