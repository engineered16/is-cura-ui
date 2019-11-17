#   __init__.py
#   Teton Simulation
#   Authored on   November 16, 2019
#   Last Modified November 16, 2019

from .SmartSliceModifierMesh import SmartSliceModifierMesh

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("smartslice")


def getMetaData():
    return {
        "scene_node": {
            "name": i18n_catalog.i18nc("@item", "Smart Slice Modifier Mesh"),
            "weight": 15
        }
    }


def register(app):
    return {
        "scene_node": SmartSliceModifierMesh()
    }

