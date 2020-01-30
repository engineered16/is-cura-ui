# Copyright (c) 2018 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.


#   Filesystem Control
import os.path

#  Ultimaker Imports
from UM.i18n import i18nCatalog

from UM.Application import Application
from UM.Version import Version
from UM.PluginRegistry import PluginRegistry
from UM.Logger import Logger
from UM.Event import Event, MouseEvent, KeyEvent
from UM.Tool import Tool
from UM.Math.Vector import Vector
from UM.Signal import Signal

from UM.View.GL.OpenGL import OpenGL
from UM.Scene.Selection import Selection
from UM.Scene.SceneNode import SceneNode

from cura.Scene.CuraSceneNode import CuraSceneNode

#  QT / QML Imports
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtQml import QQmlComponent, QQmlContext # @UnresolvedImport

#  Local Imports
from .SmartSliceSelectHandle import SelectionMode
from .SmartSliceSelectHandle import SmartSliceSelectHandle
#from .SmartSliceDrawSelection import SmartSliceSelectionVisualizer
from .FaceSelection import SelectablePoint, SelectableFace, SelectableMesh
#from .SmartSliceNormalArrow import SmartSliceNormalArrow

i18n_catalog = i18nCatalog("smartslice")

##  Provides the tool to rotate meshes and groups
#
#   The tool exposes a ToolHint to show the rotation angle of the current operation
class SmartSliceSelectTool(Tool):
    def __init__(self, extension):
        super().__init__()
        self.extension = extension
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
        self._scene_node_name = None
        self._selectable_mesh = None

        self._controller.activeToolChanged.connect(self._onActiveStateChanged)


    ##  Handle mouse and keyboard events
    #
    #   \param event type(Event)
    def event(self, event):
        return super().event(event)

    def _calculateMesh(self):
        nodes = Selection.getAllSelectedObjects()

        if len(nodes) > 0:
            sn = nodes[0]

            if self._scene_node_name is None or sn.getName() != self._scene_node_name:

                mesh_data = nodes[0].getMeshData()

                if mesh_data:
                    Logger.log('d', 'Compute SelectableMesh from SceneNode {}'.format(sn.getName()))
                    
                    self._scene_node_name = sn.getName()
                    self._selectable_mesh = SelectableMesh(mesh_data)

                    controller = Application.getInstance().getController()
                    camTool = controller.getCameraTool()
                    camTool.setOrigin(self._selectable_mesh.box.center)

    def _onSelectedFaceChanged(self):
        curr_sf = Selection.getSelectedFace()
        #cloud_connector = PluginRegistry.getInstance().getPluginObject("SmartSlicePlugin").cloud
        cloud_connector = self.extension.cloud

        if curr_sf is not None and self._selectable_mesh is not None:
            scene_node, face_id = curr_sf

            selmesh = self._selectable_mesh
            
            #  Construct Selectable Face && Draw Selection in canvas
            #sf = SelectableFace(tri_pts, mesh_data._normals, face_id)

            # Get the SelectableFace by matching the face Id - is this consistent??
            sf = selmesh.faces[face_id]

            self.selected_faces = [sf] # TODO: Rewrite for >1 concurrently selected faces
            #self._visualizer.changeSelection([sf])

            self._handle.setFace(sf)

            #  If Load Mode is Active
            if self.getLoadSelectionActive():
                #  Set/Draw Load Selection in Scene
                self._handle.drawFaceSelection(SelectionMode.LoadMode, selmesh, draw_arrow=True)

            #  If Anchor Mode is Active
            else:
                #  Set/Draw Anchor Selection in Scene
                self._handle.drawFaceSelection(SelectionMode.AnchorMode, selmesh)

            self._handle.scale(scene_node.getScale(), transform_space=CuraSceneNode.TransformSpace.World)

            # Passing our infos to the CloudConnector
            
            # # Direction should only matter here.
            # # The location is given by the faces I assume
            load_vector = self._handle.getLoadVector()
            # -> After clicking on a face, I get a crash below, that my load_vector is None.
            
            if load_vector and self._handle._connector._proxy.loadMagnitudeInverted:
                load_vector = load_vector * -1
            
            loaded_faces = [face._id for face in self._handle._loaded_faces]
            anchored_faces = [face._id for face in self._handle._anchored_faces]
            Logger.log("d", "loaded_faces: {}".format(loaded_faces))
            Logger.log("d", "anchored_faces: {}".format(anchored_faces))
            
            if self._selection_mode is SelectionMode.AnchorMode:
                print ("\n\nANCHOR APPLIED RIGHT HERE\n\n")
                cloud_connector._proxy._anchorsApplied = 1

                #
                #   TODO: Change _anchorsApplied from ' = 1' to arbitrary # of loads
                #           * Check for multiple selection key, e.g. Shift
                #
                
                cloud_connector.appendAnchor0FacesPoc(anchored_faces)
                Logger.log("d", "cloud_connector.getAnchor0FacesPoc(): {}".format(cloud_connector.getAnchor0FacesPoc()))

                Application.getInstance().activityChanged.emit()
            else:
                print ("\nLOAD APPLIED RIGHT HERE\n\n")
                cloud_connector._proxy._loadsApplied = 1

                #
                #   TODO: Change _loadsApplied from ' = 1' to arbitrary # of loads
                #           * Check for multiple selection key, e.g. Shift
                #

                cloud_connector.setForce0VectorPoc(load_vector.x,
                                                   load_vector.y,
                                                   load_vector.z
                                                   )
                cloud_connector.appendForce0FacesPoc(loaded_faces)
                Logger.log("d", "cloud_connector.getForce0VectorPoc(): {}".format(cloud_connector.getForce0VectorPoc()))
                Logger.log("d", "cloud_connector.getForce0FacesPoc(): {}".format(cloud_connector.getForce0FacesPoc()))

                Application.getInstance().activityChanged.emit()
            

    def _onActiveStateChanged(self):
        controller = Application.getInstance().getController()
        active_tool = controller.getActiveTool()
        Logger.log("d", "Application.getInstance().getController().getActiveTool(): {}".format(active_tool))

        if active_tool == self and Selection.hasSelection():
            Selection.setFaceSelectMode(True)
            Logger.log("d", "Enabled faceSelectMode!")
        else:
            Selection.setFaceSelectMode(False)
            Logger.log("d", "Disabled faceSelectMode!")

        self._calculateMesh()

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
        self._handle.clearSelection()
        self._handle.paintAnchoredFaces()
        self.setSelectionMode(SelectionMode.AnchorMode)

    def getAnchorSelectionActive(self):
        return self._selection_mode is SelectionMode.AnchorMode

    def setLoadSelection(self):
        self._handle.clearSelection()
        self._handle.paintLoadedFaces()
        self.setSelectionMode(SelectionMode.LoadMode)

    def getLoadSelectionActive(self):
        return self._selection_mode is SelectionMode.LoadMode
