# Copyright (c) 2018 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.


#   Filesystem Control
import os.path

#  Ultimaker Imports
from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("smartslice")

from UM.Application import Application
from UM.Version import Version
from UM.PluginRegistry import PluginRegistry
from UM.Logger import Logger
from UM.Event import Event, MouseEvent, KeyEvent

from UM.Tool import Tool

from UM.View.GL.OpenGL import OpenGL
from UM.Scene.Selection import Selection
from UM.Scene.SceneNode import SceneNode

#  QT / QML Imports
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtQml import QQmlComponent, QQmlContext # @UnresolvedImport

#  Local Imports
from .SmartSliceSelectHandle import SmartSliceSelectHandle
#from .SmartSliceDrawSelection import SmartSliceSelectionVisualizer
from .FaceSelection import SelectablePoint, SelectableEdge, SelectableFace
from .FaceSelection import fromMeshData
#from .SmartSliceNormalArrow import SmartSliceNormalArrow


# Provides enums
class SelectionMode:
    AnchorMode = 1
    LoadMode = 2


##  Provides the tool to rotate meshes and groups
#
#   The tool exposes a ToolHint to show the rotation angle of the current operation
class SmartSliceSelectTool(Tool):
    def __init__(self):
        super().__init__()
        self._handle = SmartSliceSelectHandle()

        #self._shortcut_key = Qt.Key_S

        self._selection_mode = SelectionMode.AnchorMode
        self.setExposedProperties("AnchorSelectionActive",
                                  "LoadSelectionActive",
                                  "SelectionMode",
                                  )

        Selection.selectedFaceChanged.connect(self._onSelectedFaceChanged)
        self.selected_face = None   # DEPRECATED
        self.selected_faces = []
        self.selectable_faces = []

        self._scene = self.getController().getScene()

        self._controller.activeToolChanged.connect(self._onActiveStateChanged)

        #  Create new 'Selection Visualizer' with no faces actively selected
        #  TODO:  Return to this after conference
        #print("\n")
        #self._visualizer = SmartSliceSelectionVisualizer()
        #self.getController().getScene().getRoot().addChild(self._visualizer)
        #Logger.log("d", "Enabling Selection Vizualizer")
        
        #  Create new Normal Arrow for vizualising selected face normal vector
        #self._normal_arrow = SmartSliceNormalArrow()
        #Logger.log("d", "Creating Normal Arrow Mesh")
        #print("\n")


    ##  Handle mouse and keyboard events
    #
    #   \param event type(Event)
    def event(self, event):
        super().event(event)

        """
        if event.type == Event.KeyPressEvent and event.key == KeyEvent.ShiftKey:
            Logger.log("d", "Enabling faceSelectMode!")
            #Selection.setFaceSelectMode(True)
        if event.type == Event.KeyReleaseEvent and event.key == KeyEvent.ShiftKey:
            Logger.log("d", "Disabling faceSelectMode!")
            #Selection.setFaceSelectMode(False)
        """
        
        if event.type == Event.MousePressEvent:
            if MouseEvent.LeftButton not in event.buttons:
                return False

            #id = self._selection_pass.getIdAtPosition(event.x, event.y)
            #if not id:
            #    return False

        
            """
            if self._handle.isAxis(id):
                self.setLockedAxis(id)
            else:
                # Not clicked on an axis: do nothing.
                return False
            handle_position = self._handle.getWorldPosition()
            """

            """
            if Selection.hasSelection() and not Selection.getFaceSelectMode():
                Selection.setFaceSelectMode(True)
                Logger.log("d", "Enabled faceSelectMode!")
            elif not Selection.getSelectedFace() and Selection.getFaceSelectMode():
                Selection.setFaceSelectMode(False)
                Logger.log("d", "Disabled faceSelectMode!")
            """
        
            if Selection.getSelectedFace() is not None:
                Logger.log("d", "Selection.getSelectedFace(): {}".format(Selection.getSelectedFace()[0]))

            return True
            

        if event.type == Event.MouseReleaseEvent:
            # Finish a rotate operation
            if len(self.selected_faces) > 0:
                '''Application.getInstance().messageBox("SmartSlice",
                                                     "You selected face: {}\ngetFaceSelectMode={}".format(self.selected_face,
                                                                                                          Selection.getFaceSelectMode()
                                                                                                          )
                                                     )'''

            return True

    def _onSelectedFaceChanged(self):
        curr_sf = Selection.getSelectedFace()
        if curr_sf is not None:

            scene_node, face_id = curr_sf
            mesh_data = scene_node.getMeshData()
            selectable_faces = fromMeshData(mesh_data)

            norms = []

            #print(dir(scene_node.getMeshData()))
            
            #if not mesh_data._indices or len(mesh_data._indices) == 0:
            if (mesh_data._indices is None) or (len(mesh_data._indices) == 0):
                base_index = face_id * 3
                v_a = mesh_data._vertices[base_index]
                n_a = mesh_data._normals[base_index]
                v_b = mesh_data._vertices[base_index+1]
                n_b = mesh_data._normals[base_index+1]
                v_c = mesh_data._vertices[base_index+2]
                n_c = mesh_data._normals[base_index+2]
            else:
                v_a = mesh_data._vertices[mesh_data._indices[face_id][0]]
                n_a = mesh_data._normals[mesh_data._indices[face_id][0]]
                v_b = mesh_data._vertices[mesh_data._indices[face_id][1]]
                n_b = mesh_data._normals[mesh_data._indices[face_id][1]]
                v_c = mesh_data._vertices[mesh_data._indices[face_id][2]]
                n_c = mesh_data._normals[mesh_data._indices[face_id][2]]
            
            p0 = SelectablePoint(float(v_a[0]), float(v_a[1]), float(v_a[2]), n_a)
            p1 = SelectablePoint(float(v_b[0]), float(v_b[1]), float(v_b[2]), n_b)
            p2 = SelectablePoint(float(v_c[0]), float(v_c[1]), float(v_c[2]), n_c)
            
            #  Construct Selectable Face && Draw Selection in canvas
            sf = SelectableFace([p0, p1, p2],
                                mesh_data._normals)
            self.selected_faces = [sf] # TODO: Rewrite for >1 concurrently selected faces
            #self._visualizer.changeSelection([sf])

            self._handle.setFace(sf)

            if self.getLoadSelectionActive():
                self._handle.drawFaceSelection(draw_arrow=True, other_faces=selectable_faces)
            else:
                self._handle.drawFaceSelection(other_faces=selectable_faces)
                
            


            '''
            print("v_a", v_a)
            print("v_b", v_b)
            print("v_c", v_c)
            '''


    def _onActiveStateChanged(self):
        active_tool = Application.getInstance().getController().getActiveTool()
        Logger.log("d", "Application.getInstance().getController().getActiveTool(): {}".format(Application.getInstance().getController().getActiveTool()))

        if active_tool == self and Selection.hasSelection():
            Selection.setFaceSelectMode(True)
            Logger.log("d", "Enabled faceSelectMode!")
        else:
            Selection.setFaceSelectMode(False)
            Logger.log("d", "Disabled faceSelectMode!")

    ##  Get whether the select face feature is supported.
    #   \return True if it is supported, or False otherwise.
    def getSelectFaceSupported(self) -> bool:
        # Use a dummy postfix, since an equal version with a postfix is considered smaller normally.
        return Version(OpenGL.getInstance().getOpenGLVersion()) >= Version("4.1 dummy-postfix")
    
    def setSelectionMode(self, mode):
        if self._selection_mode is not mode:
            self._selection_mode = mode
            
            Logger.log("d", "Changed selection mode to enum: {}".format(mode))

    def getSelectionMode(self):
        return self._selection_mode

    def setAnchorSelection(self):
        self.setSelectionMode(SelectionMode.AnchorMode)

    def getAnchorSelectionActive(self):
        return self._selection_mode is SelectionMode.AnchorMode

    def setLoadSelection(self):
        self.setSelectionMode(SelectionMode.LoadMode)

    def getLoadSelectionActive(self):
        return self._selection_mode is SelectionMode.LoadMode
