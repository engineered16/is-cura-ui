import os
import sys

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("smartslice")
from UM.Logger import Logger

from .utils import SystemUtils

# Loading third party modules
third_party_dir = os.path.realpath(__file__)
third_party_dir = os.path.dirname(third_party_dir)
third_party_dir = os.path.join(third_party_dir, "3rd-party")
if os.path.isdir(third_party_dir):
    SystemUtils.registerThirdPartyModules(third_party_dir)

# Importing pywim for testing
import pywim

from . import SmartSliceExtension
from .requirements_tool import SmartSliceRequirements
from .select_tool import SmartSliceSelectTool
from .stage import SmartSliceStage

extension = SmartSliceExtension.SmartSliceExtension()
#extension._name = "Extension"
requirements_tool = SmartSliceRequirements.SmartSliceRequirements(extension)
requirements_tool._name = "RequirementsTool"
select_tool = SmartSliceSelectTool.SmartSliceSelectTool(extension)
select_tool._name = "SelectTool"

def getMetaData():
    return {
        "stage": {
            "name": i18n_catalog.i18nc("@item:inmenu", "Smart Slice"),
            "weight": 15
        },
        "tool": [{"name": i18n_catalog.i18nc("@label", "Smart Slice Requirements"),
                  "description": i18n_catalog.i18nc("@info:tooltip", "Allows user to set safety factor and maximum deflection"),
                  "icon": "requirements_tool/tool_icon.svg",
                  "tool_panel": "requirements_tool/SmartSliceRequirements.qml",
                  "weight": 20
                  },
                 {"name": i18n_catalog.i18nc("@label", "Smart Slice SelectTool"),
                  "description": i18n_catalog.i18nc("@info:tooltip", "Allows user to set boundaries on a model."),
                  "icon": "select_tool/tool_icon.svg",
                  "tool_panel": "select_tool/SmartSliceSelectTool.qml",
                  "weight": 10
                  }
                 ]
    }


def register(app):
    return {
        "extension": extension,
        "stage": SmartSliceStage.SmartSliceStage(extension.cloud),
        "tool": [requirements_tool,
                 select_tool,
                 ]
    }
