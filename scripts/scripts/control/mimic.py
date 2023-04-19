from .behaviour import Behaviour
from .emotion import EmotionBehaviour, Emotion
from core import Robot, State
from recognition import faceFromImage

class MimicBehaviour(Behaviour):
    """
    Makes the robot imitate the person in front of it.
    """

    def __init__(self):
        self.emotion = EmotionBehaviour()

    def update(self, robot: Robot) -> State:
        # Perceive the emotion of the person in front of the robot
        person_emotion = perceive_emotion(robot)

        # Detect features of the person's face (e.g. eyes open/closed, direction)
        person_features = detect_face_features(robot)

        # Make the robot imitate these features
        imitate_features(robot, person_features)

        state = robot.getActualState() # placeholder while the behaviour is not implemented
        face = faceFromImage(robot.getFrame())
        return state.mix(self.emotion.update(robot), 0.5)

    def perceive_emotion(robot: Robot) -> Emotion:
        # TODO: Implement emotion perception using the robot's sensors
        return Emotion.neutral

    def detect_face_features(robot: Robot) -> dict:
        # TODO: Implement face feature detection using the robot's sensors
        return {}

    def imitate_features(robot: Robot, features: dict):
        # TODO: Implement feature imitation using the robot's actuators
        pass