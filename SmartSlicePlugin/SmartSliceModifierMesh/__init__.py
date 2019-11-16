from .SmartSliceModifierMesh import SmartSliceModifierMesh

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("smartslice")


def getMetaData():
    return {
        "plugin_object": {
            "name": i18n_catalog.i18nc("@label", "Smart Slice ModifierMesh"),
            "description": i18n_catalog.i18nc("@info:tooltip", "Allows visualization of intelligent slice Modifier Mesh")
        }
    }


def register(app):
    return {
        "plugin_object": SmartSliceModifierMesh()
    }
