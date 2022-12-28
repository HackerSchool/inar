from .behaviour import Behaviour
from .emotion import EmotionBehaviour, Emotion
from core import Robot, State

class MimicBehaviour(Behaviour):
    """
    Makes the robot imitate the person in front of it.
    """

    def __init__(self):
        self.emotion = EmotionBehaviour()

    def update(self, robot: Robot) -> State:
        # TODO: perceive the emotion of the person in front of the robot
        # TODO: detect features of the person's face (e.g. eyes open/closed, direction)
        # TODO: make the robot imitate these features
        state = robot.getActualState() # placeholder while the behaviour is not implemented
        return state.mix(self.emotion.update(robot), 0.5)
