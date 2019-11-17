# PreviewModifierMesh.py
# Teton Simulation
# Authored on   November 16, 2019
# Last Modified November 17, 2019


#
#   Create mod meshes, place on build plate, reslice, and push user to "Preview" stage
#


from UM.Application import Application
from UM.Scene import Scene


class PreviewModifierMesh:
    def __init__(self, parent=None):
        super().__init__()

        #  Default Properties
        self._controller = Application.getInstance().getController()
        self._parent = parent # Reference to SmartSliceModifierMesh


    '''
      preview()

        Moves the user into the 'Preview' Stage
    '''
    def preview(self):
        self._controller.setActiveStage("Preview")


