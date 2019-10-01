#   Constraints.py
#   Teton Simulation, Inc
#   Authored on   October 1, 2019
#   Last Modified October 1, 2019


#
#   Contains generalized structure/properties of a Constraint
#
#   A constraint can be:
#     * Anchors (Static Subcomponents)
#     * Loads (Neutonian Forces)
#


class _SmartSliceConstraint:
  def __init__(self, parent = None):
    #  STUB STUB STUB
    super().__init__(parent)

    #  Set Default Properties
    self._constraint_type = "Unset"

