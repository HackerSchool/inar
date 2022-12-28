from core import Robot, State

class Behaviour:
    """
    Contains the logic for controlling the robot in a specific way.
    """

    def update(self, robot: Robot) -> State:
        """
        Returns robot stote desired by this behaviour.
        """
        raise NotImplementedError
