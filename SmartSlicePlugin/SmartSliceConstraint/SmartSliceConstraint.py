#   SmartSliceConstraint.py
#   Teton Simulation, Inc
#   Authored on   October 1, 2019
#   Last Modified October 1, 2019

#
#   Contains generalized interface for handling Boundary Conditions (Constraints) within a Smart Slice use case. 
#
#   A constraint can be:
#     * Anchors (Static Subcomponents)
#     * Loads (Neutonian Forces)
#


#   API Imports
from .Anchors import SmartSliceAnchor
from .Loads import SmartSliceLoad



class SmartSliceConstraint:
  def __init__(self, parent = None):
    #  STUB STUB STUB
    super().__init__(parent)




