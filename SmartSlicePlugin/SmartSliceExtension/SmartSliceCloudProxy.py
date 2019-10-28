'''
Created on 22.10.2019

@author: thopiekar
'''

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QTime

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

        # Properties (mainly) for the sliceinfo widget
        self._resultSafetyFactor = 1.0
        self._resultMaximalDisplacement = 2
        self._resultTimeInfill = QTime(0, 0, 0, 1)
        self._resultTimeInnerWalls = QTime(0, 0, 0, 1)
        self._resultTimeOuterWalls = QTime(0, 0, 0, 1)
        self._resultTimeRetractions = QTime(0, 0, 0, 1)
        self._resultTimeSkin = QTime(0, 0, 0, 1)
        self._resultTimeSkirt = QTime(0, 0, 0, 1)
        self._resultTimeTravel = QTime(0, 0, 0, 1)
        self._resultTimes = (self._resultTimeInfill,
                             self._resultTimeInnerWalls,
                             self._resultTimeOuterWalls,
                             self._resultTimeRetractions,
                             self._resultTimeSkin,
                             self._resultTimeSkirt,
                             self._resultTimeTravel,
                             )
        self._percentageTimeInfill = 0.0
        self._percentageTimeInnerWalls = 0.0
        self._percentageTimeOuterWalls = 0.0
        self._percentageTimeRetractions = 0.0
        self._percentageTimeSkin = 0.0
        self._percentageTimeSkirt = 0.0
        self._percentageTimeTravel = 0.0
        
        self.resultTimeInfillChanged.connect(self._onResultTimeChanged)
        self.resultTimeInnerWallsChanged.connect(self._onResultTimeChanged)
        self.resultTimeOuterWallsChanged.connect(self._onResultTimeChanged)
        self.resultTimeRetractionsChanged.connect(self._onResultTimeChanged)
        self.resultTimeSkinChanged.connect(self._onResultTimeChanged)
        self.resultTimeSkirtChanged.connect(self._onResultTimeChanged)
        self.resultTimeTravelChanged.connect(self._onResultTimeChanged)

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

    # Properties (mainly) for the sliceinfo widget

    resultSafetyFactorChanged = pyqtSignal()

    @pyqtProperty(float, notify=resultSafetyFactorChanged)
    def resultSafetyFactor(self):
        return self._resultSafetyFactor

    @resultSafetyFactor.setter
    def resultSafetyFactor(self, value):
        if self._resultSafetyFactor is not value:
            Logger.log("d", "resultSafetyFactor: <{}> -> <{}>".format(self._resultSafetyFactor, value))
            self._resultSafetyFactor = value
            self.resultSafetyFactorChanged.emit()

    resultMaximalDisplacementChanged = pyqtSignal()

    @pyqtProperty(int, notify=resultMaximalDisplacementChanged)
    def resultMaximalDisplacement(self):
        return self._resultMaximalDisplacement

    @resultMaximalDisplacement.setter
    def resultMaximalDisplacement(self, value):
        if self._resultMaximalDisplacement is not value:
            Logger.log("d", "resultMaximalDisplacement: <{}> -> <{}>".format(self._resultMaximalDisplacement, value))
            self._resultMaximalDisplacement = value
            self.resultMaximalDisplacementChanged.emit()

    resultTimeInfillChanged = pyqtSignal()

    @pyqtProperty(QTime, notify=resultTimeInfillChanged)
    def resultTimeInfill(self):
        return self._resultTimeInfill

    @resultTimeInfill.setter
    def resultTimeInfill(self, value: QTime):
        if self._resultTimeInfill is not value:
            Logger.log("d", "resultTimeInfill: <{}> -> <{}>".format(self._resultTimeInfill, value))
            self._resultTimeInfill = value
            self.resultTimeInfillChanged.emit()

    resultTimeInnerWallsChanged = pyqtSignal()

    @pyqtProperty(QTime, notify=resultTimeInnerWallsChanged)
    def resultTimeInnerWalls(self):
        return self._resultTimeInnerWalls

    @resultTimeInnerWalls.setter
    def resultTimeInnerWalls(self, value: QTime):
        if self._resultTimeInnerWalls is not value:
            Logger.log("d", "resultTimeInnerWalls: <{}> -> <{}>".format(self._resultTimeInnerWalls, value))
            self._resultTimeInnerWalls = value
            self.resultTimeInnerWallsChanged.emit()

    resultTimeOuterWallsChanged = pyqtSignal()

    @pyqtProperty(QTime, notify=resultTimeOuterWallsChanged)
    def resultTimeOuterWalls(self):
        return self._resultTimeOuterWalls

    @resultTimeOuterWalls.setter
    def resultTimeOuterWalls(self, value: QTime):
        if self._resultTimeOuterWalls is not value:
            Logger.log("d", "resultTimeOuterWalls: <{}> -> <{}>".format(self._resultTimeOuterWalls, value))
            self._resultTimeOuterWalls = value
            self.resultTimeOuterWallsChanged.emit()

    resultTimeRetractionsChanged = pyqtSignal()

    @pyqtProperty(QTime, notify=resultTimeRetractionsChanged)
    def resultTimeRetractions(self):
        return self._resultTimeRetractions

    @resultTimeRetractions.setter
    def resultTimeRetractions(self, value: QTime):
        if self._resultTimeRetractions is not value:
            Logger.log("d", "resultTimeRetractions: <{}> -> <{}>".format(self._resultTimeRetractions, value))
            self._resultTimeRetractions = value
            self.resultTimeRetractionsChanged.emit()

    resultTimeSkinChanged = pyqtSignal()

    @pyqtProperty(QTime, notify=resultTimeSkinChanged)
    def resultTimeSkin(self):
        return self._resultTimeSkin

    @resultTimeSkin.setter
    def resultTimeSkin(self, value: QTime):
        if self._resultTimeSkin is not value:
            Logger.log("d", "resultTimeSkin: <{}> -> <{}>".format(self._resultTimeSkin, value))
            self._resultTimeSkin = value
            self.resultTimeSkinChanged.emit()

    resultTimeSkirtChanged = pyqtSignal()

    @pyqtProperty(QTime, notify=resultTimeSkirtChanged)
    def resultTimeSkirt(self):
        return self._resultTimeSkirt

    @resultTimeSkirt.setter
    def resultTimeSkirt(self, value: QTime):
        if self._resultTimeSkirt is not value:
            Logger.log("d", "resultTimeSkirt: <{}> -> <{}>".format(self._resultTimeSkirt, value))
            self._resultTimeSkirt = value
            self.resultTimeSkirtChanged.emit()

    resultTimeTravelChanged = pyqtSignal()

    @pyqtProperty(QTime, notify=resultTimeTravelChanged)
    def resultTimeTravel(self):
        return self._resultTimeTravel

    @resultTimeTravel.setter
    def resultTimeTravel(self, value: QTime):
        if self._resultTimeTravel is not value:
            Logger.log("d", "resultTimeTravel: <{}> -> <{}>".format(self._resultTimeTravel, value))
            self._resultTimeTravel = value
            self.resultTimeTravelChanged.emit()

    percentageTimeInfillChanged = pyqtSignal()

    @pyqtProperty(float, notify=percentageTimeInfillChanged)
    def percentageTimeInfill(self):
        return self._percentageTimeInfill

    @percentageTimeInfill.setter
    def percentageTimeInfill(self, value):
        if not self._percentageTimeInfill == value:
            Logger.log("d", "percentageTimeInfill: <{}> -> <{}>".format(self._percentageTimeInfill, value))
            self._percentageTimeInfill = value
            self.percentageTimeInfillChanged.emit()

    percentageTimeInnerWallsChanged = pyqtSignal()

    @pyqtProperty(float, notify=percentageTimeInnerWallsChanged)
    def percentageTimeInnerWalls(self):
        return self._percentageTimeInnerWalls

    @percentageTimeInnerWalls.setter
    def percentageTimeInnerWalls(self, value):
        if not self._percentageTimeInnerWalls == value:
            Logger.log("d", "percentageTimeInnerWalls: <{}> -> <{}>".format(self._percentageTimeInnerWalls, value))
            self._percentageTimeInnerWalls = value
            self.percentageTimeInnerWallsChanged.emit()

    percentageTimeOuterWallsChanged = pyqtSignal()

    @pyqtProperty(float, notify=percentageTimeOuterWallsChanged)
    def percentageTimeOuterWalls(self):
        return self._percentageTimeOuterWalls

    @percentageTimeOuterWalls.setter
    def percentageTimeOuterWalls(self, value):
        if not self._percentageTimeOuterWalls == value:
            Logger.log("d", "percentageTimeOuterWalls: <{}> -> <{}>".format(self._percentageTimeOuterWalls, value))
            self._percentageTimeOuterWalls = value
            self.percentageTimeOuterWallsChanged.emit()

    percentageTimeRetractionsChanged = pyqtSignal()

    @pyqtProperty(float, notify=percentageTimeRetractionsChanged)
    def percentageTimeRetractions(self):
        return self._percentageTimeRetractions

    @percentageTimeRetractions.setter
    def percentageTimeRetractions(self, value):
        if not self._percentageTimeRetractions == value:
            Logger.log("d", "percentageTimeRetractions: <{}> -> <{}>".format(self._percentageTimeRetractions, value))
            self._percentageTimeRetractions = value
            self.percentageTimeRetractionsChanged.emit()

    percentageTimeSkinChanged = pyqtSignal()

    @pyqtProperty(float, notify=percentageTimeSkinChanged)
    def percentageTimeSkin(self):
        return self._percentageTimeSkin

    @percentageTimeSkin.setter
    def percentageTimeSkin(self, value):
        if not self._percentageTimeSkin == value:
            Logger.log("d", "percentageTimeSkin: <{}> -> <{}>".format(self._percentageTimeSkin, value))
            self._percentageTimeSkin = value
            self.percentageTimeSkinChanged.emit()

    percentageTimeSkirtChanged = pyqtSignal()

    @pyqtProperty(float, notify=percentageTimeSkirtChanged)
    def percentageTimeSkirt(self):
        return self._percentageTimeSkirt

    @percentageTimeSkirt.setter
    def percentageTimeSkirt(self, value):
        if not self._percentageTimeSkirt == value:
            Logger.log("d", "percentageTimeSkirt: <{}> -> <{}>".format(self._percentageTimeSkirt, value))
            self._percentageTimeSkirt = value
            self.percentageTimeSkirtChanged.emit()

    percentageTimeTravelChanged = pyqtSignal()

    @pyqtProperty(float, notify=percentageTimeTravelChanged)
    def percentageTimeTravel(self):
        return self._percentageTimeTravel

    @percentageTimeTravel.setter
    def percentageTimeTravel(self, value):
        if not self._percentageTimeTravel == value:
            Logger.log("d", "percentageTimeTravel: <{}> -> <{}>".format(self._percentageTimeTravel, value))
            self._percentageTimeTravel = value
            self.percentageTimeTravelChanged.emit()
            
    def _onResultTimeChanged(self):
        total_time = 0
        
        #for result_time in self._resultTimes:
        #    total_time += result_time.msecsSinceStartOfDay()
        
        total_time += self.resultTimeInfill.msecsSinceStartOfDay()
        total_time += self.resultTimeInnerWalls.msecsSinceStartOfDay()
        total_time += self.resultTimeOuterWalls.msecsSinceStartOfDay()
        total_time += self.resultTimeRetractions.msecsSinceStartOfDay()
        total_time += self.resultTimeSkin.msecsSinceStartOfDay()
        total_time += self.resultTimeSkirt.msecsSinceStartOfDay()
        total_time += self.resultTimeTravel.msecsSinceStartOfDay()
        
        self.percentageTimeInfill = 100.0 / total_time * self.resultTimeInfill.msecsSinceStartOfDay()
        self.percentageTimeInnerWalls = 100.0 / total_time * self.resultTimeInnerWalls.msecsSinceStartOfDay()
        self.percentageTimeOuterWalls = 100.0 / total_time * self.resultTimeOuterWalls.msecsSinceStartOfDay()
        self.percentageTimeRetractions = 100.0 / total_time * self.resultTimeRetractions.msecsSinceStartOfDay()
        self.percentageTimeSkin = 100.0 / total_time * self.resultTimeSkin.msecsSinceStartOfDay()
        self.percentageTimeSkirt = 100.0 / total_time * self.resultTimeSkirt.msecsSinceStartOfDay()
        self.percentageTimeTravel = 100.0 / total_time * self.resultTimeTravel.msecsSinceStartOfDay()
