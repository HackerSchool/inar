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
        # Change the state of the robot according to the emotion
        if self.emotion == Emotion.NEUTRAL:
            # TODO: implement the neutral behavior
            pass
        elif self.emotion == Emotion.HAPPY:
            # TODO: implement the happy behavior
            pass
        elif self.emotion == Emotion.SAD:
            # TODO: implement the sad behavior
            pass
        elif self.emotion == Emotion.ANGRY:
            # TODO: implement the angry behavior
            pass
        elif self.emotion == Emotion.SURPRISED:
            # TODO: implement the surprised behavior
            pass
        return robot.getActualState()
