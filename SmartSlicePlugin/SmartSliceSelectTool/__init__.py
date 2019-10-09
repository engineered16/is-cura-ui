from .SmartSliceSelectTool import SmartSliceSelectTool

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("smartslice")


def getMetaData():
    return {
        "tool": {
            "name": i18n_catalog.i18nc("@label", "Smart Slice SelectTool"),
            "description": i18n_catalog.i18nc("@info:tooltip", "Allows user to set boundaries on a model."),
            "icon": "tool_icon.svg",
            "weight": 10
        }
    }


def register(app):
    return {
        "tool": SmartSliceSelectTool()
    }
