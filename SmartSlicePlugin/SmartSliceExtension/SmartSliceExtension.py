import os

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
        
        # Login Window
        self._login_dialog = None
        #self.addMenuItem(i18n_catalog.i18n("Login"),
        #                 self._openLoginDialog)

    def _openLoginDialog(self):
        if not self._login_dialog:
            self._login_dialog, self._login_context, self._login_component = self._createQmlDialog("SmartSliceCloudLogin.qml")
        self._login_dialog.show()

    def _createQmlDialog(self, dialog_qml, directory = None):
        if directory is None:
            directory = PluginRegistry.getInstance().getPluginPath(self.getPluginId())
        path = QUrl.fromLocalFile(os.path.join(directory, dialog_qml))
        component = QQmlComponent(Application.getInstance()._qml_engine, path)

        # We need access to engine (although technically we can't)
        context = QQmlContext(Application.getInstance()._qml_engine.rootContext())
        #context.setContextProperty("manager", self)
        dialog = component.create(context)
        if dialog is None:
            Logger.log("e", "QQmlComponent status %s", component.status())
            Logger.log("e", "QQmlComponent errorString %s", component.errorString())
        return dialog, context, component

    def _onEngineCreated(self):
        self.cloud._onEngineCreated()
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

    def getProxy(self, engine, script_engine):
        return self._proxy

    def getVariables(self, engine, script_engine):
        return self._variables
