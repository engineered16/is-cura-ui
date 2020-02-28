from PyQt5.QtCore import QAbstractListModel, QObject, QModelIndex
from PyQt5.QtCore import pyqtProperty, pyqtSlot

from UM.Logger import Logger
from UM.Scene.Selection import Selection

from cura.CuraApplication import CuraApplication

from ..utils import findChildSceneNode
from ..stage import SmartSliceScene

class BoundaryConditionListModel(QAbstractListModel):
    Anchor = 0
    Force = 1

    def __init__(self, parent=None):
        super().__init__(parent)

        # TODO can we get rid of self._bcs and dynamically return
        # the data in self.data() from digging into self._smart_slice_node?
        # Will the ordering of the children scene nodes be predictable?

        self._bcs = []
        self._bc_type = BoundaryConditionListModel.Anchor
        self._smart_slice_scene_node = None
        self._active_node = None

    def _populateList(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._bcs) - 1)
        self._bcs.clear()
        self.endRemoveRows()

        #scene = CuraApplication.getInstance().getController().getScene().getRoot()
        selected_node = Selection.getSelectedObject(0)

        if not selected_node:
            Logger.warning("No node selected for creating boundary conditions")
            return

        self._smart_slice_scene_node = findChildSceneNode(selected_node, SmartSliceScene.Root)

        if not self._smart_slice_scene_node:
            Logger.warning("No SmartSlice node found for creating boundary conditions")
            return

        if self._bc_type == BoundaryConditionListModel.Anchor:
            node_type = SmartSliceScene.AnchorFace
        else:
            node_type = SmartSliceScene.LoadFace

        for c in self._smart_slice_scene_node.getChildren():
            c.setActiveSelect(False)
            if isinstance(c, node_type):
                self._bcs.append(c)

        self.beginInsertRows(QModelIndex(), 0, len(self._bcs) - 1)
        self.endInsertRows()

        if len(self._bcs) > 0:
            self._bcs[0].setActiveSelect(True)

    def getActiveNode(self):
        return self._active_node

    def roleNames(self):
        return {
            0: b'name'
        }

    @pyqtProperty(int)
    def boundaryConditionType(self) -> int:
        return self._bc_type

    @boundaryConditionType.setter
    def boundaryConditionType(self, value : int):
        self._bc_type = value
        self._populateList()

    @pyqtProperty(bool)
    def loadDirection(self) -> bool:
        if isinstance(self._active_node, SmartSliceScene.LoadFace):
            return self._active_node.force.pull
        return False

    @loadDirection.setter
    def loadDirection(self, value : bool):
        if isinstance(self._active_node, SmartSliceScene.LoadFace):
            self._active_node.setArrowDirection(value)

    @pyqtProperty(float)
    def loadMagnitude(self) -> float:
        if isinstance(self._active_node, SmartSliceScene.LoadFace):
            return self._active_node.force.magnitude
        return 0.0

    @loadMagnitude.setter
    def loadMagnitude(self, value : float):
        if isinstance(self._active_node, SmartSliceScene.LoadFace):
            self._active_node.force.magnitude = value

    @pyqtSlot(QObject, result=int)
    def rowCount(self, parent=None) -> int:
        return len(self._bcs)

    def data(self, index, role):
        if len(self._bcs) > index.row():
            if role == 0:
                return self._bcs[index.row()].getName()
        return None

    @pyqtSlot()
    def activate(self):
        self.select()

    @pyqtSlot()
    def add(self):
        N = len(self._bcs)
        self.beginInsertRows(QModelIndex(), N, N)

        # TODO - how to keep track of bc # to avoid duplicate
        # names from deleting a bc in the middle and then adding a new one?

        if self._bc_type == BoundaryConditionListModel.Anchor:
            bc = SmartSliceScene.AnchorFace('Anchor ' + str(N))
        else:
            bc = SmartSliceScene.LoadFace('Load ' + str(N))
            bc.force.magnitude = 10.0

        self._smart_slice_scene_node.addChild(bc)
        self._bcs.append(bc)

        self.endInsertRows()

    @pyqtSlot(int)
    def remove(self, index=None):
        if index is not None and len(self._bcs) > index:
            self.beginRemoveRows(QModelIndex(), index, index)

            self._smart_slice_scene_node.removeChild(self._bcs[index])
            
            del self._bcs[index]

            self._active_node = None

            self.endRemoveRows()

    @pyqtSlot(int)
    def select(self, index=None):
        if index is not None and len(self._bcs) > index:
            self._active_node = self._bcs[index]

        active_tool = CuraApplication.getInstance().getController().getActiveTool()

        if active_tool:
            active_tool.setActiveBoundaryConditionList(self)
