'''
Created on 22.10.2019

@author: thopiekar
'''

from PyQt5.QtCore import pyqtSignal, pyqtProperty, QObject


from UM.Application import Application


class SmartSliceProxy(QObject):
    def __init__(self, extension, parent=None) -> None:
        super().__init__(parent)
        self.extension = extension

        self._multi_build_plate_model = Application.getInstance().activityChanged.connect(self._onSliceableNodesChanged)
        self._hasSliceableNodes = False

        #self.sendJobSignal.connect(self.extension.cloud.sendJob)

    sliceableNodesChanged = pyqtSignal()

    @pyqtProperty(bool, notify=sliceableNodesChanged)
    def hasSliceableNodes(self):
        return self._hasSliceableNodes

    @hasSliceableNodes.setter
    def hasSliceableNodes(self, value):
        self._hasSliceableNodes = value
        self.sliceableNodesChanged.emit()

    #sendJobSignal = pyqtSignal()

    def _onSliceableNodesChanged(self):
        self.hasSliceableNodes = len(self.extension.cloud.getSliceableNodes()) == 1
