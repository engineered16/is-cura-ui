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
