from .RobotframeworkRestBridgeKeywords import RobotframeworkRestBridgeKeywords
from .version import VERSION

class RestBridgeLibrary(RobotframeworkRestBridgeKeywords):
    __version__ = VERSION
    ROBOT_LIBRARY_SCOPE = "GLOBAL"