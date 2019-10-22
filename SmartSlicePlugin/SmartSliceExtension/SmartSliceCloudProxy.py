'''
Created on 22.10.2019

@author: thopiekar
'''

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import QObject

class SmartSliceCloudStatus:
    BadLogin = 1
    Ready = 2
    Sending = 3
    Waiting = 4
    Loading = 5

class SmartSliceCloudProxy(QObject):
    def __init__(self) -> None:
        super().__init__()
        
        self._status = 0
        self._maxDeflect = 2
    
    maxDeflectChanged = pyqtSignal()

    @pyqtProperty(int, notify=maxDeflectChanged)
    def maxDeflect(self):
        return self._maxDeflect
    
    @maxDeflect.setter
    def maxDeflect(self, value):
        if self._maxDeflect is not value:
            Logger.log("d", "Changing max deflect: {}->{}".format(self._maxDeflect, value))
            self._maxDeflect = value
            self.maxDeflectChanged.emit()