#   __init__.py (Constraints)
#   Teton Simulation
#   Authored on   October 5, 2019
#   Last Modified October 5, 2019

#
#   Contains the tool dialog for adding constraints (anchors/loads)
#

from .SmartSliceSelectTool import SmartSliceSelectTool

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("smartslice")


def getMetaData():
    return {
        "tool": {
            "name": i18n_catalog.i18nc("@label", "Smart Slice Set Constraints"),
            "description": i18n_catalog.i18nc("@info:tooltip", "Allows user to set boundaries on a model."),
            "icon": "tool_icon.svg",
            "weight": 20
        }
    }


def register(app):
    return {
        "tool": SmartSliceConstraints()
    }
