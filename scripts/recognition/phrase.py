from enum import Enum

class Phrase(Enum):
    """Enum for identifying different phrases that the robot can understand."""
    UNKNOWN = 0
    HI = 1
    BYE = 2
    LOOK_AT_ME = 3

    def __init__(self, phrase) -> None:
        self.phrase = phrase

    def setPhrase(self, phrase):
        self.phrase = self
    
    def getPhrase(self):
        return self.phrase
    
    def emotionFromPhrase(self):
        # TODO: implement this
