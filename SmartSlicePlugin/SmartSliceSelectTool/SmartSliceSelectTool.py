# Copyright (c) 2018 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.


from UM.Application import Application
from UM.Logger import Logger
from UM.Tool import Tool
from UM.Event import Event, MouseEvent, KeyEvent
from UM.Scene.Selection import Selection

from PyQt5.QtCore import Qt

from UM.Version import Version

from UM.View.GL.OpenGL import OpenGL

from .SmartSliceSelectHandle import SmartSliceSelectHandle

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("uranium")


##  Provides the tool to rotate meshes and groups
#
#   The tool exposes a ToolHint to show the rotation angle of the current operation
class SmartSliceSelectTool(Tool):
    def __init__(self):
        super().__init__()
        #self._handle = SmartSliceSelectHandle()

        self._shortcut_key = Qt.Key_R

        self._progress_message = None
        self._iterations = 0
        self._total_iterations = 0
        self._rotating = False
        self.setExposedProperties("SelectFaceSupported")
        self._saved_node_positions = []

        Selection.selectedFaceChanged.connect(self._onSelectedFaceChanged)
        self.selected_face = None

    ##  Handle mouse and keyboard events
    #
    #   \param event type(Event)
    def event(self, event):
        super().event(event)

        if event.type == Event.KeyPressEvent and event.key == KeyEvent.ShiftKey:
            Logger.log("d", "Enabling faceSelectMode!")
            Selection.setFaceSelectMode(True)

        if event.type == Event.KeyReleaseEvent and event.key == KeyEvent.ShiftKey:
            Logger.log("d", "Disabling faceSelectMode!")
            Selection.setFaceSelectMode(False)

        if event.type == Event.MousePressEvent and self._controller.getToolsEnabled():
            # Start a rotate operation
            if MouseEvent.LeftButton not in event.buttons:
                return False

            id = self._selection_pass.getIdAtPosition(event.x, event.y)
            if not id:
                return False

            """
            if self._handle.isAxis(id):
                self.setLockedAxis(id)
            else:
                # Not clicked on an axis: do nothing.
                return False

            handle_position = self._handle.getWorldPosition()
            """

            # Save the current positions of the node, as we want to rotate around their current centres
            self._saved_node_positions = []
            for node in self._getSelectedObjectsWithoutSelectedAncestors():
                self._saved_node_positions.append((node, node.getPosition()))

            self.setDragStart(event.x, event.y)
            self._rotating = False
            return True

        if event.type == Event.MouseReleaseEvent:
            # Finish a rotate operation
            if self.selected_face:
                Application.getInstance().messageBox("SmartSlice",
                                                     "You selected face: {}\ngetFaceSelectMode={}".format(self.selected_face,
                                                                                                          Selection.getFaceSelectMode()
                                                                                                          )
                                                     )
    def _onSelectedFaceChanged(self):
        # Keeping tool handle disabled for now
        #self._handle.setEnabled(not Selection.getFaceSelectMode())

        if Selection.getFaceSelectMode() and Selection.hasSelection():
            self.selected_face = Selection.getSelectedFace()
        else:
            self.selected_face = None

        Logger.log("d", "getFaceSelectMode: {}".format(Selection.getFaceSelectMode()))
        Logger.log("d", "getHoverFace: {}".format(Selection.getHoverFace()))
        if not self.selected_face:
            # Just an early exit for some code below...
            return



    ##  Get whether the select face feature is supported.
    #   \return True if it is supported, or False otherwise.
    def getSelectFaceSupported(self) -> bool:
        # Use a dummy postfix, since an equal version with a postfix is considered smaller normally.
        return Version(OpenGL.getInstance().getOpenGLVersion()) >= Version("4.1 dummy-postfix")
