#   SmartSliceRequirements.py
#   Teton Simulation
#   Authored on   October 8, 2019
#   Last Modified October 8, 2019

#
#   Contains definitions for the "Requirements" Tool, which serves as an interface for requirements
#
#   Types of Requirements:
#     * Safety Factor
#     * Maximum Deflection
#

#   Ultimaker/Cura Imports
from UM.Application import Application
from UM.Tool import Tool
from UM.Signal import Signal


#   Smart Slice Requirements Tool:
#     When Pressed, this tool produces the "Requirements Dialog"
#
class SmartSliceRequirements(Tool):
    #  Class Initialization
    def __init__(self):
        super().__init__()

        # Internals
        self._savetyFactor = 1.0
        self._maxDeflect = 2

        # Signals to deliever values to our engine
        self.signalSafetyFactorChanged = Signal()
        self.signalMaxDeflectChanged = Signal()

        # Register our properties and passively tell Cura that the get* and set* functions below exist
        self.setExposedProperties("SafetyFactor", "MaxDeflect")

        Application.getInstance().engineCreatedSignal.connect(self._onEngineCreated)

    def getSafetyFactor(self):
        return self._savetyFactor

    def setSafetyFactor(self, factor):
        if self._savetyFactor is not factor:
            self._savetyFactor = factor
            self.signalSafetyFactorChanged.emit(factor)

    def getMaxDeflect(self):
        return self._maxDeflect

    def setMaxDeflect(self, length):
        if self._maxDeflect is not length:
            self._maxDeflect = length
            self.signalMaxDeflectChanged.emit(length)

    def _onEngineCreated(self):
        # Letting our general extension know which defaults we have here.
        self.signalMaxDeflectChanged.emit(self._savetyFactor)
        self.signalMaxDeflectChanged.emit(self._maxDeflect)
        Application.getInstance().getController().addTool(self) #  TESTING
