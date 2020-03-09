from UM.Tool import Tool

#   Smart Slice Requirements Tool:
#     When Pressed, this tool produces the "Requirements Dialog"
#
class SmartSliceRequirements(Tool):
    #  Class Initialization
    def __init__(self, extension):
        super().__init__()

        self._connector = extension.cloud
