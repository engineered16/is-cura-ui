#   Loads.py
#   Teton Simulation, Inc
#   Authored on   October 1, 2019
#   Last Modified October 1, 2019


#
#   Contains interface functionality for setting/releasing Neutonian Forces (LOADS)
#
#   A load is a force of specified magnitude applied normal to a surface.  
#   Multiple loads can be applied to a part and a final NET FORCE is displayed with an arrow for each subcomponent (upon selection).
#   If the existing loads and anchors create a conflict or break in a part, the overall USE CASE is reported as 'INVALID'.
#


#   API Imports
from .Constraints import _SmartSliceConstraint


#   A LOAD is a property that can be applied to a subcomponent on a model, 
#     where a neutonian force is applied normal to a selected surface.
#     The force can either be a push or a pull (i.e. towards external/internal face)
class SmartSliceLoad:
  def __init__(self, parent = _SmartSliceConstraint):
    #  STUB STUB STUB
    super().__init__(parent)

    self._constraint_type = "Load"

