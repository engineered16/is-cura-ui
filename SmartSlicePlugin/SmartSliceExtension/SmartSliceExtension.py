from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtQml import qmlRegisterSingletonType

from UM.Application import Application
from UM.Extension import Extension
from UM.Qt.Bindings.ToolModel import ToolModel

class SmartSliceProxy(QObject):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

    @pyqtSlot(int, result = bool)
    def selectedTool(self):
        return True

class ToolModel(ToolModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.clear()
        
    def _onToolsChanged(self):
        pass

class SmartSliceExtension(Extension):

    def __init__(self):
        super().__init__()

        Application.getInstance().engineCreatedSignal.connect(self._onEngineCreated)

        self._proxy = SmartSliceProxy()
        self._toolModel = ToolModel()

    def getTools(self):
        return self._toolset

    def _onEngineCreated(self):
        qmlRegisterSingletonType(SmartSliceProxy, "SmartSlice", 1, 0, "Proxy", self.getProxy)
        qmlRegisterSingletonType(SmartSliceProxy, "SmartSlice", 1, 0, "ToolModel", self.getToolModel)

    def getProxy(self, engine, script_engine):
        return self._proxy

    def getToolModel(self, engine, script_engine):
        return self._toolModel