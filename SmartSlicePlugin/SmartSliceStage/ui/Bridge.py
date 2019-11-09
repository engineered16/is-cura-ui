#   bridge.py
#   Teton Simulation
#   Authored on   October 16, 2019
#   Last Modified October 16, 2019


#
#   Contains python-side interface for bridge between Smart Slice API/Engine to Javascript
#


from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject

from .Compat import ApplicationCompat
from PyQt5.QtQml import QQmlContext # @UnresolvedImport

class SmartSliceBridge(QObject):
    def __init__(self): 
        QObject.__init__(self)

        _context = QQmlContext(ApplicationCompat().qml_engine.rootContext())
        _context.setContextProperty("_bridge", self)

    #    
    #  ACCESSORS
    #

    #  SAFETY FACTOR
    @pyqtSlot()
    def _SafetyFactorComputed(self):
        return "2.5"

    @pyqtSlot()
    def _SafetyFactorTarget(self):
        return "> 4"

    #  MAXIMUM DISPLACEMENT
    def _MaxDeflectionComputed(self):
        return "5  mm"

    def _MaxDeflectionTarget(self):
        return "> 2mm"


