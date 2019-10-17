#   bridge.py
#   Teton Simulation
#   Authored on   October 16, 2019
#   Last Modified October 16, 2019


#
#   Contains python-side interface for bridge between Smart Slice API/Engine to Javascript
#

from UM.Application import Application



class SmartSliceBridge(object):
    def __init__(self, parent=None): 
        self._x = 1 + 1

    #    
    #  ACCESSORS
    #

    #  SAFETY FACTOR
    def _SafetyFactorComputed():
        return 2.5

    def _SafetyFactorTarget():
        return "> 4"

    #  MAXIMUM DISPLACEMENT
    def _MaxDeflectionComputed():
        return "5  mm"

    def _MaxDeflectionTarget():
        return "> 2mm"


