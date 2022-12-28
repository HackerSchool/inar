from .behaviour import Behaviour
from core import Robot, State
from recognition import Emotion

class EmotionBehaviour(Behaviour):
    """
    Controls the robot using predefined emotions.
    """

    def __init__(self):
        self.emotion = Emotion.NEUTRAL

    def setEmotion(self, emotion: Emotion):
        """
        Sets the emotion that should be displayed.
        """
        self.emotion = emotion

    def update(self, robot: Robot) -> State:
        # TODO: change the state of the robot according to the emotion
        return robot.getActualState()
