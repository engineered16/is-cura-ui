#   __init__.py (SmartSliceRequirements.py)
#   Teton Simulation
#   Authored on   October 8, 2019
#   Last Modified October 8, 2019

#
#   Contains the tool dialog for adding requirements (safety/deflection)
#

from .SmartSliceRequirements import SmartSliceRequirements

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("smartslice")


def getMetaData():
    return {
        "tool": {
            "name": i18n_catalog.i18nc("@label", "Smart Slice Requirements"),
            "description": i18n_catalog.i18nc("@info:tooltip", "Allows user to set safety factor and maximum deflection"),
            "icon": "tool_icon.svg",
            "weight": 20
        }
    }


def register(app):
    return {
        "tool": SmartSliceRequirements()
    }
