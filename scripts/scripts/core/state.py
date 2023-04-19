from enum import Enum

class Servo(Enum):
    """Enum for identifying servos."""
    L_EYE_X = 0 # -90º to 90º
    L_EYE_Y = 1 # -90º to 90º
    R_EYE_X = 2 # -90º to 90º
    R_EYE_Y = 3 # -90º to 90º
    L_LID   = 4 # 0 to 1
    R_LID   = 5 # 0 to 1
    
class State:
    """Holds the state of the robot's servos."""

    def __init__(self):
        self.positions = [0 for servo in Servo]

    def lookAt(self, point: (float, float, float)):
        """
        Rotates the eye servos so that they point at a specific point.
        The coordinate system of the point is such that X is right, Y is up, Z
        is forward. One unit is equal to the distance between the eyes' centers.
        The position between the eyes is (0, 0, 0).
        """
        # TODO: Implement this
        pass

    def mix(self, other, factor):
        """
        Returns a new state that is a mix of this state and another state.
        The factor parameter specifies the weight of the other state.
        """
        result = State()
        for servo in Servo:
            result.setPosition(servo, self.getPosition(servo) * (1 - factor) + other.getPosition(servo) * factor)
        return result

    def update(self, target, deltaT: float):
        """
        Moves this state towards the target state taking into account the time
        since the last update.
        """
        for servo in Servo:
            # Stupid interpolation, we need to enhance this in the future
            # Certain servos (like the eye servos) should receive special treatment.
            diff = target.getPosition(servo) - self.getPosition(servo)
            new = self.getPosition(servo) + diff * min(deltaT, 1.0)
            self.setPosition(servo, new)

    def setPosition(self, servo, position):
        """Sets the position of a servo."""
        self.positions[servo.value] = position

    def getPosition(self, servo):
        """Gets the position of a servo."""
        return self.positions[servo.value]
