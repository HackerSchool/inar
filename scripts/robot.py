from state import State

class Robot:
    """
    Represents the robot's hardware and abstracts away the details of
    controlling it.
    """

    def __init__(self):
        self.targetState = State()
        self.actualState = State()
        self.frame = None
        self.socket = None

    def update(self, deltaT):
        """
        Updates the robot, given the time passed since the last update.
        """
        self.actualState.update(self.targetState, deltaT) 

    def setTargetState(self, state):
        """Sets the target state of the robot."""
        self.targetState = state
    
    def setActualState(self, state):
        """Sets the current state of the robot."""
        self.actualState = state

    def getActualState(self):
        """Returns the current state of the robot."""
        return self.actualState

    def setFrame(self, frame):
        self.frame = frame

    def getFrame(self):
        """Returns the last frame captured by the robot's camera."""
        return self.frame
