from enum import Enum

class Phrase(Enum):
    """Enum for identifying different phrases that the robot can understand."""
    UNKNOWN = 0
    HI = 1
    BYE = 2
    LOOK_AT_ME = 3
