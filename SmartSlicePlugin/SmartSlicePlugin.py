import os.path

from UM.Logger import Logger
from UM.Application import Application
from UM.PluginRegistry import PluginRegistry
from UM.Scene.Iterator.DepthFirstIterator import DepthFirstIterator

from cura.Stages.CuraStage import CuraStage
from cura.Scene.CuraSceneNode import CuraSceneNode
from cura.Scene.BuildPlateDecorator import BuildPlateDecorator


class SmartSliceStage(CuraStage):
    def __init__(self, parent=None):
        super().__init__(parent)

        Application.getInstance().engineCreatedSignal.connect(self._engineCreated)

        self._was_buildvolume_hidden = None
        self._was_presliced = None

    def onStageSelected(self):
        buildvolume = Application.getInstance().getBuildVolume()
        if buildvolume.isVisible():
            buildvolume.setVisible(False)
            self._was_buildvolume_hidden = True
            
        print_information = Application.getInstance().getPrintInformation()
        if not print_information.preSliced:
            print_information.setPreSliced(True)
            self._was_presliced = False
        

    def onStageDeselected(self):
        if self._was_buildvolume_hidden:
            buildvolume = Application.getInstance().getBuildVolume()
            buildvolume.setVisible(True)
            self._is_buildvolume_hidden = None
            
        if not self._was_presliced:
            print_information = Application.getInstance().getPrintInformation()
            if print_information.preSliced:
                print_information.setPreSliced(False)
            self._was_presliced = True

    def _engineCreated(self):

        base_path = PluginRegistry.getInstance().getPluginPath("SmartSlicePlugin")
        menu_component_path = os.path.join(base_path, "ui", "SmartSliceMenu.qml")
        main_component_path = os.path.join(base_path, "ui", "SmartSliceMain.qml")
        self.addDisplayComponent("menu", menu_component_path)
        self.addDisplayComponent("main", main_component_path)
