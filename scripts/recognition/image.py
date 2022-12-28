from .face import Face
from .emotion import Emotion

def faceFromImage(image) -> Face:
    """
    Extracts the facial features from an image of a face.
    Its assumed that the image has been cropped to the face's region.
    """
    face = Face()
    # TODO: implement this
    return face

def emotionFromImage(image) -> Emotion:
    """
    Extracts the emotion from an image of a face.
    Its assumed that the image has been cropped to the face's region.
    """
    emotion = Emotion.NEUTRAL
    # TODO: implement this
    return emotion
