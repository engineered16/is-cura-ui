import os
import json

from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterSingletonType
from PyQt5.QtQml import QQmlContext
from PyQt5.QtQml import QQmlComponent

from UM.i18n import i18nCatalog
from UM.Application import Application
from UM.Extension import Extension
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry

from .SmartSliceProxy import SmartSliceProxy
from .SmartSliceCloudConnector import SmartSliceCloudConnector
from .SmartSliceVariables import SmartSliceVariables

i18n_catalog = i18nCatalog("smartslice")

class SmartSliceExtension(Extension):
    def __init__(self):
        super().__init__()

        # Proxy, which serves all variables
        self._variables = SmartSliceVariables()

        # Separate module for cloud connection
        self.cloud = SmartSliceCloudConnector(self)

        # General proxy for everything that is not specific
        self._proxy = SmartSliceProxy(self)

        Application.getInstance().engineCreatedSignal.connect(self._onEngineCreated)

        #self.setMenuName(i18n_catalog.i18nc("@item:inmenu", "Smart Slice"))

        # About Dialog
        self._about_dialog = None
        self.addMenuItem(i18n_catalog.i18nc("@item:inmenu", "About"), self._openAboutDialog)
        
        # Login Window
        self._login_dialog = None
        #self.addMenuItem(i18n_catalog.i18n("Login"),
        #                 self._openLoginDialog)


    def _openLoginDialog(self):
        if not self._login_dialog:
            self._login_dialog = self._createQmlDialog("SmartSliceCloudLogin.qml")
        self._login_dialog.show()

    def _openAboutDialog(self):
        if not self._about_dialog:
            self._about_dialog = self._createQmlDialog("SmartSliceAbout.qml", vars={"aboutText": self._aboutText()})
        self._about_dialog.show()

    def _closeAboutDialog(self):
        if not self._about_dialog:
            self._about_dialog.close()

    def _createQmlDialog(self, dialog_qml, directory = None, vars = None):
        if directory is None:
            directory = PluginRegistry.getInstance().getPluginPath(self.getPluginId())

        mainApp = Application.getInstance()

        return mainApp.createQmlComponent(os.path.join(directory, dialog_qml), vars)

    def _onEngineCreated(self):
        # Registering our type in QML for direct interaction.
        # Needed for separate windows for example.
        # NOTE: Unused at the moment!
        qmlRegisterSingletonType(SmartSliceProxy,
                                 "SmartSlice",
                                 1, 0,
                                 "Proxy",
                                 self.getProxy
                                 )
        '''
        qmlRegisterSingletonType(SmartSliceVariables,
                                 "SmartSlice",
                                 1, 0,
                                 "Variables",
                                 self.getVariables
                                 )
        '''

    def _aboutText(self):
        about = 'Smart Slice for Cura\n'

        try:
            plugin_json_path = os.path.dirname(os.path.abspath(__file__))
            plugin_json_path = os.path.join(plugin_json_path, 'plugin.json')
            with open(plugin_json_path, 'r') as f:
                plugin_info = json.load(f)
            about += 'Version: {}'.format(plugin_info['version'])
        except:
            pass

        return about

    def getProxy(self, engine, script_engine):
        return self._proxy

    def getVariables(self, engine, script_engine):
        return self._variables
