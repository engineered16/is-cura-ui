import os
import sys

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("smartslice")
from UM.Logger import Logger

#from .utils import SystemUtils

# Loading third party modules
third_party_dir = os.path.realpath(__file__)
third_party_dir = os.path.dirname(third_party_dir)
third_party_dir = os.path.join(third_party_dir, "3rd-party")
#if os.path.isdir(third_party_dir):
    #SystemUtils.registerThirdPartyModules(third_party_dir)

# Importing pywim for testing
import pywim

from . import SmartSliceExtension

def getMetaData():
    return {
        "stage": {
            "name": i18n_catalog.i18nc("@item:inmenu", "Smart Slice"),
            "weight": 15
        }
    }


def register(app):
    return {
        "extension": SmartSliceExtension.SmartSliceExtension()
    }
