from . import SmartSlicePlugin

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("smartslice")


def getMetaData():
    return {
        "stage": {
            "name": i18n_catalog.i18nc("@item:inmenu", "Smart Slice"),
            "weight": 15
        }
    }


def register(app):
    return {
        "stage": SmartSlicePlugin.SmartSliceStage()
    }
