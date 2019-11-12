# SmartSliceSelectHandle.py
# Teton Simulation
# Last Modified November 12, 2019

# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.

#
#   Contains functionality to be triggered upon face selection
#

from UM.Scene.ToolHandle import ToolHandle
from UM.Mesh.MeshBuilder import MeshBuilder
from UM.Math.Vector import Vector

class SmartSliceSelectHandle(ToolHandle):
    def __init__(self, parent = None):
        super().__init__(parent)

        self._name = "SmartSliceSelectHandle"

        self._line_width = 0.5
        self._active_line_width = 1.0
        self.color = self.AllAxisSelectionColor


    def displaySelectedFace(self):
        1 + 1 # STUB

    def displayNormalArrow(self):
        1 + 1

