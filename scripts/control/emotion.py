from .behaviour import Behaviour
from core import Robot, State
from recognition import Emotion
import random

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
        state = robot.getActualState()
        if self.emotion == Emotion.NEUTRAL:
            # Set eye lids to half closed
            state.setPosition(State.Servo.L_LID, 0.5)
            state.setPosition(State.Servo.R_LID, 0.5)
            # Look straight ahead
            state.lookAt((0, 0, 1))
        elif self.emotion == Emotion.HAPPY:
            # Open eye lids
            state.setPosition(State.Servo.L_LID, 0)
            state.setPosition(State.Servo.R_LID, 0)
            # Look slightly up and to the right
            state.lookAt((0.5, 0.3, 0.8))
        elif self.emotion == Emotion.SAD:
            # Close eye lids
            state.setPosition(State.Servo.L_LID, 1)
            state.setPosition(State.Servo.R_LID, 1)
            # Look slightly down
            state.lookAt((0, -0.2, 1))
        elif self.emotion == Emotion.ANGRY:
            # Lower left eye lid
            state.setPosition(State.Servo.L_LID, 0.8)
            state.setPosition(State.Servo.R_LID, 0.5)
            # Look slightly down and to the left
            rand_factor = random.uniform(0.1, 0.2)
            state.lookAt((-0.5*rand_factor, -0.2, 1-rand_factor))
        elif self.emotion == Emotion.SURPRISED:
            # Open eye lids wide
            state.setPosition(State.Servo.L_LID, 0)
            state.setPosition(State.Servo.R_LID, 0)
            # Look up and to the right
            rand_factor = random.uniform(0.1, 0.3)
            state.lookAt((0.7*rand_factor, 0.7*rand_factor, 0.7-0.5*rand_factor))
        return state