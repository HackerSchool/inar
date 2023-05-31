from enum import Enum
from typing import Tuple
import math

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

    def lookAt(self, point: Tuple[float, float, float]):
        """
        Rotates the eye servos so that they point at a specific point.
        The coordinate system of the point is such that X is right, Y is up, Z
        is forward. One unit is equal to the distance between the eyes' centers.
        The position between the eyes is (0, 0, 0).
        """
        x, y, z = point

        # Calculates the horizontal angles for the left and right servos
        angle_x_left = math.atan2(y, x - 1)
        angle_x_right = math.atan2(y, x + 1)

        # Calculate vertical angles for left and right eye servos
        angle_y_left = math.atan2(z, math.sqrt(x ** 2 + y ** 2))
        angle_y_right = math.atan2(z, math.sqrt(x ** 2 + y ** 2))

        # Set the calculated angles in the servo positions
        self.positions[Servo.L_EYE_X.value] = math.degrees(angle_x_left)
        self.positions[Servo.R_EYE_X.value] = math.degrees(angle_x_right)
        self.positions[Servo.L_EYE_Y.value] = math.degrees(angle_y_left)
        self.positions[Servo.R_EYE_Y.value] = math.degrees(angle_y_right)

        return x, y, z

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
