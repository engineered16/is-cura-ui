import os
import tempfile
import json
import zipfile

from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtQml import qmlRegisterSingletonType

from UM.Application import Application
from UM.Extension import Extension
from UM.Logger import Logger
from UM.Mesh.MeshWriter import MeshWriter
from UM.PluginRegistry import PluginRegistry
from UM.Scene.Iterator.DepthFirstIterator import DepthFirstIterator


class SmartSliceProxy(QObject):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    @pyqtSlot(int, result=bool)
    def selectedTool(self):
        return True


class SmartSliceAwsConnector():
    def __init__(self):
        self._savetyFactor = None
        self._maxDeflect = None

    def _onEngineCreated(self):
        # Connecting to signals of our Requirements tool
        Logger.log("d", "Connecting to Qt Signals of SmartSliceRequirements")
        requirements_tool = PluginRegistry.getInstance().getPluginObject("SmartSliceRequirements")
        requirements_tool.signalSafetyFactorChanged.connect(self.setSafetyFactor)
        requirements_tool.signalMaxDeflectChanged.connect(self.setMaxDeflect)

    def setSafetyFactor(self, factor):
        Logger.log("d", "SafetyFactor: {}".format(factor))
        self._savetyFactor = factor

    def setMaxDeflect(self, length):
        Logger.log("d", "MaxDeflect: {}".format(length))
        self._maxDeflect = length

    def getSliceableNodes(self):
        scene_node = Application.getInstance().getController().getScene().getRoot()
        sliceable_nodes = []

        for node in DepthFirstIterator(scene_node):
            if node.callDecoration("isSliceable"):
                sliceable_nodes.append(node)

        return sliceable_nodes

    def prepareInitial3mf(self):
        # Using tempfile module to probe for a temporary file path
        # TODO: We can do this more elegant of course, too.
        file = tempfile.NamedTemporaryFile(suffix=".3mf")
        filename = file.name
        del(file)
        Logger.log("d", "filename: {}".format(filename))

        # Checking whether count of models == 1
        mesh_nodes = self.getSliceableNodes()
        if len(mesh_nodes) is not 1:
            Logger.log("d", "Found {} meshes!".format(["no", "too many"][len(mesh_nodes) > 1]))
            return None

        # Getting 3MF writer and write our file
        threeMF_Writer = PluginRegistry.getInstance().getPluginObject("3MFWriter")
        threeMF_Writer.write(filename, mesh_nodes)

        return filename

    def appendTo3mf(self, filename):
        requirements = {
            "savety_factor": self._savetyFactor,
            "max_deflect": self._maxDeflect,
            }
        json_data = json.dumps(requirements,
                               # Some optional formatting for the json file
                               indent=4,
                               )
        threemf_file = zipfile.ZipFile(filename,
                                       "a",
                                       compression=zipfile.ZIP_DEFLATED,
                                       )
        json_zip_content = zipfile.ZipInfo("Teton/requirements.json")
        json_zip_content.compress_type = zipfile.ZIP_DEFLATED
        threemf_file.writestr(json_zip_content, json_data)

        return filename

    def sendJob(self):
        filename = self.prepareInitial3mf()

        if not filename:
            return None

        self.appendTo3mf(filename)

        # SEND YOUR 3MF TO THE CLOUD HERE

        # PROCESS THE DIRECT RESPONSE AND/OR WAIT

        # EMITTING A SIGNAL WITH THE RESULTS AND DISPLAY THEM IN QML


class SmartSliceExtension(Extension, SmartSliceAwsConnector):
    def __init__(self):
        Extension.__init__(self)
        SmartSliceAwsConnector.__init__(self)

        self._proxy = SmartSliceProxy()

        Application.getInstance().engineCreatedSignal.connect(self._onEngineCreated)

    def _onEngineCreated(self):
        SmartSliceAwsConnector._onEngineCreated(self)
        # Registering our type in QML for direct interaction. Needed for separate windows for example.
        # NOTE: Unused at the moment!
        qmlRegisterSingletonType(SmartSliceProxy,
                                 "SmartSlice",
                                 1, 0,
                                 "Proxy",
                                 self.getProxy
                                 )

    def getProxy(self, engine, script_engine):
        return self._proxy
