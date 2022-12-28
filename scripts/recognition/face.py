from enum import Enum

class Feature(Enum):
    """Enum for identifying different facial features."""
    L_EYE_X    = 0 # -90º to 90º
    L_EYE_Y    = 1 # -90º to 90º
    R_EYE_X    = 2 # -90º to 90º
    R_EYE_Y    = 3 # -90º to 90º
    L_EYE_OPEN = 4 # 0 to 1
    R_EYE_OPEN = 5 # 0 to 1

class Face:
    """
    Holds the facial features extracted from an image of a face.
    """

    def __init__(self):
        self.features = [0 for feature in Feature]

    def setFeature(self, feature, value):
        """Sets the value of a facial feature."""
        self.features[feature.value] = value

    def getFeature(self, feature):
        """Gets the value of a facial feature."""
        return self.features[feature.value]

