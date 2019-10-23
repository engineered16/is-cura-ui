from PyQt5.QtQml import qmlRegisterSingletonType

from UM.Application import Application
from UM.Extension import Extension
from UM.Logger import Logger

from .SmartSliceProxy import SmartSliceProxy
from .SmartSliceCloudConnector import SmartSliceCloudConnector
from .SmartSliceVariables import SmartSliceVariables


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
        qmlRegisterSingletonType(SmartSliceVariables,
                                 "SmartSlice",
                                 1, 0,
                                 "Variables",
                                 self.getVariables
                                 )

    def getProxy(self, engine, script_engine):
        return self._proxy

    def getVariables(self, engine, script_engine):
        return self._variables
