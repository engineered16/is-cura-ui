'''
Created on 22.10.2019

@author: thopiekar
'''

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import QObject

from UM.Logger import Logger

class SmartSliceCloudStatus:
    NoConnection = 1
    BadLogin = 2
    InvalidInput = 3
    ReadyToVerify = 4
    Underdimensioned = 5
    Overdimensioned = 6
    BusyValidating = 7
    BusyOptimizing = 8
    Optimized = 9

    Busy = (BusyValidating,
            BusyOptimizing,
            )

    Optimizable = (Underdimensioned,
                   Overdimensioned,
                   )


class SmartSliceCloudProxy(QObject):
    def __init__(self, connector) -> None:
        super().__init__()
        
        self.connector = connector

        # Properties (mainly) for the login window
        self._loginStatus = "Please log in with your credentials below."
        self._loginName = ""
        self._loginPassword = ""

        # Properties (mainly) for the sliceinfo popup
        self._sliceStatus = "_Status"
        self._sliceHint = "_Hint"
        self._sliceButtonText = "_ButtonText"
        self._sliceButtonEnabled = False
        self._sliceIconImage = ""
        self._sliceIconVisible = False

    # Properties (mainly) for the login window

    loginStatusChanged = pyqtSignal()

    @pyqtProperty(str, notify=loginStatusChanged)
    def loginStatus(self):
        return self._loginStatus

    @loginStatus.setter
    def loginStatus(self, value):
        if self._loginStatus is not value:
            Logger.log("d", "loginStatus: <{}> -> <{}>".format(self._loginStatus, value))
            self._loginStatus = value
            self.loginStatusChanged.emit()

    loginNameChanged = pyqtSignal()

    @pyqtProperty(str, notify=loginNameChanged)
    def loginName(self):
        return self._loginName

    @loginName.setter
    def loginName(self, value):
        if self._loginName is not value:
            Logger.log("d", "loginName: <{}> -> <{}>".format(self._loginName, value))
            self._loginName = value
            self.loginNameChanged.emit()

    loginPasswordChanged = pyqtSignal()

    @pyqtProperty(str, notify=loginPasswordChanged)
    def loginPassword(self):
        return self._loginPassword

    @loginPassword.setter
    def loginPassword(self, value):
        if self._loginPassword is not value:
            Logger.log("d", "loginPassword: <secret!>")
            self._loginPassword = value
            self.loginPasswordChanged.emit()
            
    @pyqtProperty(bool, notify=loginPasswordChanged)
    def loginResult(self):
        return self.connector.login()

    # Properties (mainly) for the sliceinfo widget

    sliceStatusChanged = pyqtSignal()

    @pyqtProperty(str, notify=sliceStatusChanged)
    def sliceStatus(self):
        return self._sliceStatus

    @sliceStatus.setter
    def sliceStatus(self, value):
        if self._sliceStatus is not value:
            Logger.log("d", "sliceStatus: <{}> -> <{}>".format(self._sliceStatus, value))
            self._sliceStatus = value
            self.sliceStatusChanged.emit()

    sliceHintChanged = pyqtSignal()

    @pyqtProperty(str, notify=sliceHintChanged)
    def sliceHint(self):
        return self._sliceHint

    @sliceHint.setter
    def sliceHint(self, value):
        if self._sliceHint is not value:
            Logger.log("d", "sliceHint: <{}> -> <{}>".format(self._sliceHint, value))
            self._sliceHint = value
            self.sliceHintChanged.emit()

    sliceButtonTextChanged = pyqtSignal()

    @pyqtProperty(str, notify=sliceButtonTextChanged)
    def sliceButtonText(self):
        return self._sliceButtonText

    @sliceButtonText.setter
    def sliceButtonText(self, value):
        if self._sliceButtonText is not value:
            Logger.log("d", "sliceButtonText: <{}> -> <{}>".format(self._sliceButtonText, value))
            self._sliceButtonText = value
            self.sliceButtonTextChanged.emit()

    sliceButtonEnabledChanged = pyqtSignal()

    @pyqtProperty(bool, notify=sliceButtonEnabledChanged)
    def sliceButtonEnabled(self):
        return self._sliceButtonEnabled

    @sliceButtonEnabled.setter
    def sliceButtonEnabled(self, value):
        if self._sliceButtonEnabled is not value:
            Logger.log("d", "sliceButtonEnabled: <{}> -> <{}>".format(self._sliceButtonEnabled, value))
            self._sliceButtonEnabled = value
            self.sliceButtonEnabledChanged.emit()
            
    sliceButtonClicked = pyqtSignal()

    sliceIconImageChanged = pyqtSignal()

    @pyqtProperty(str, notify=sliceIconImageChanged)
    def sliceIconImage(self):
        return self._sliceIconImage

    @sliceIconImage.setter
    def sliceIconImage(self, value):
        if self._sliceIconImage is not value:
            Logger.log("d", "sliceIconImage: <{}> -> <{}>".format(self._sliceIconImage, value))
            self._sliceIconImage = value
            self.sliceIconImageChanged.emit()

    sliceIconVisibleChanged = pyqtSignal()

    @pyqtProperty(bool, notify=sliceIconVisibleChanged)
    def sliceIconVisible(self):
        return self._sliceIconVisible

    @sliceIconVisible.setter
    def sliceIconVisible(self, value):
        if self._sliceIconVisible is not value:
            Logger.log("d", "sliceIconVisible: <{}> -> <{}>".format(self._sliceIconVisible, value))
            self._sliceIconVisible = value
            self.sliceIconVisibleChanged.emit()
