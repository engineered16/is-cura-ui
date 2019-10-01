#   Anchors.py
#   Teton Simulation, Inc
#   Authored on   October 1, 2019
#   Last Modified October 1, 2019


#
#   Contains interface functionality for setting/releasing Anchor Points
#
#   An Anchor Point serves as a locational constraint for a subcomponent.
#   Once loads are applied to a part, the anchored components will be marked as STATIC.
#   If it is not possible for an anchor to be maintained under the given use case, the part should be marked as 'INVALID'
#


#   API Imports
from .Constraints import _SmartSliceConstraint


#   An ANCHOR is a property that can be applied to a subcomponent on a model, 
#     where said subcomponent MUST remain static or an invalidity is reported in the use case.
#     After an anchor is applied, the forces assume only unanchored parts can still be affected by the force.
class SmartSliceAnchor:
  def __init__(self, parent = _SmartSliceConstraint):
    #  STUB STUB STUB
    super().__init__(parent)

    self._constraint_type = "Anchor"
