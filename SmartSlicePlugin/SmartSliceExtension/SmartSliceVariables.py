'''
Created on 22.10.2019

@author: thopiekar
'''

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import QObject

from UM.Logger import Logger


class SmartSliceVariables(QObject):
    def __init__(self) -> None:
        super().__init__()

        self._safetyFactor = 1.0
        self._maxDeflect = 2

    maxDeflectChanged = pyqtSignal()

    @pyqtProperty(float, notify=maxDeflectChanged)
    def maxDeflect(self):
        return self._maxDeflect

    @maxDeflect.setter
    def maxDeflect(self, value):
        if self._maxDeflect is not value:
            Logger.log("d", "Changing max deflect: {}->{}".format(self._maxDeflect, value))
            self._maxDeflect = value
            self.maxDeflectChanged.emit()

    safetyFactorChanged = pyqtSignal()

    @pyqtProperty(float, notify=safetyFactorChanged)
    def safetyFactor(self):
        return self._safetyFactor

    @safetyFactor.setter
    def safetyFactor(self, value):
        if self._safetyFactor is not value:
            Logger.log("d", "Changing safety factor: {}->{}".format(self._safetyFactor, value))
            self._safetyFactor = value
            self.safetyFactorChanged.emit()
