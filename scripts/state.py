from enum import Enum

class Servo(Enum):
    """Enum for identifying servos."""
    L_EYE_X = 0 # -90º to 90º
    L_EYE_Y = 1 # -90º to 90º
    R_EYE_X = 2 # -90º to 90º
    R_EYE_Y = 3 # -90º to 90º

class State:
    """Holds the state of the robot's servos."""

    def __init__(self):
        self.positions = [0 for s in Servo]

    def setPosition(self, servo, position):
        """Sets the position of a servo."""
        self.positions[servo.value] = position

    def getPosition(self, servo):
        """Gets the position of a servo."""
        return self.positions[servo.value]
