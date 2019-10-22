'''
Created on 22.10.2019

@author: thopiekar
'''

import os
import tempfile
import json
import zipfile

from UM.Application import Application
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry
from UM.Preferences import Preferences
from UM.Scene.Iterator.DepthFirstIterator import DepthFirstIterator

from .SmartSliceCloudProxy import SmartSliceCloudStatus
from .SmartSliceCloudProxy import SmartSliceCloudProxy 

class SmartSliceAwsConnector():
    def __init__(self, extension):
        self.extension = extension
        
        self.token = Preferences.getInstance().getValue("SmartSlice/CloudToken")
        self._proxy = SmartSliceCloudProxy()
        
    @property
    def variables(self):
        return self.extension.getVariables(None, None)

    def _onEngineCreated(self):
        self._proxy.status = SmartSliceCloudStatus.Ready

    def getSliceableNodes(self):
        scene_node = Application.getInstance().getController().getScene().getRoot()
        sliceable_nodes = []

        for node in DepthFirstIterator(scene_node):
            if node.callDecoration("isSliceable"):
                sliceable_nodes.append(node)

        return sliceable_nodes

    def prepareInitial3mf(self, location = None):
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

    def appendTo3mf(self, filename):
        requirements = {
            "savety_factor": self.variables.safetyFactor,
            "max_deflect": self.variables.maxDeflect,
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
        Logger.log("d", "Sending slice job!")
        filename = self.prepareInitial3mf()

        if not filename:
            return None

        self.appendTo3mf(filename)

        # SEND YOUR 3MF TO THE CLOUD HERE

        # PROCESS THE DIRECT RESPONSE AND/OR WAIT

        # EMITTING A SIGNAL WITH THE RESULTS AND DISPLAY THEM IN QML