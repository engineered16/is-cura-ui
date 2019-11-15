# SmartSliceSelectionProxy.py
# Teton Simulation
# Authored on   November 15, 2019
# Last Modified November 15, 2019

#
# Holds Python/QML Proxy for getting/setting Load Magnitude
#

import copy

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import QObject
from PyQt5.QtQml import qmlRegisterSingletonType

class SmartSliceSelectionProxy(QObject):
    def __init__(self, connector) -> None:
        super().__init__()

        self._loadMagnitude = 10.0

#  Load Magnitude Interface
    loadMagnitudeChanged = pyqtSignal()

    @pyqtProperty(float, notify=loadMagnitudeChanged)
    def loadMagnitude(self):
        return self._loadMagnitude

    @loadMagnitude.setter
    def loadMagnitude(self, value):
        if self._loadMagnitude is not value:
            self._loadMagnitude = value
            self.loadMagnitudeChanged.emit()


class SmartSliceSelectionConnector(QObject):
    def __init__(self):
        super().__init__()

        self._proxy = SmartSliceSelectionProxy(self)

    
    def getProxy(self, engine, script_engine):
        return self._proxy


    def _onEngineCreated(self):
        qmlRegisterSingletonType(SmartSliceSelectionProxy,
                                 "SmartSlice",
                                 1, 0,
                                 "Selection",
                                 self.getProxy
                                 )

