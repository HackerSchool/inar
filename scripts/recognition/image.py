from .face import Face
from .emotion import Emotion

import cv2

faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
eyesCascade = cv2.CascadeClassifier('data/haarcascade_eye_tree_eyeglasses.xml')

def cropFace(image):
    """
    Takes an image and returns a grayscale cropped image of the face.
    If no face is detected, None is returned.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = faceCascade.detectMultiScale(gray)
    if len(faces) == 0:
        return None

    # Pick the largest face
    largest = faces[0]
    for (x, y, w, h) in faces[1:]:
        if largest is None or w * h > largest[2] * largest[3]:
            largest = (x, y, w, h)

    # Crop the face
    (x, y, w, h) = largest
    return gray[y:y+h, x:x+w]

def cropEyes(image):
    """
    Takes a grayscale cropped image of a face and returns two cropped images, one for each eye.
    If no eyes are detected, None is returned.
    """
    eyes = eyesCascade.detectMultiScale(image)
    if len(eyes) != 2:
        return None

    # Pick the left and right eye
    left = eyes[0]
    right = eyes[1]
    if left[0] > right[0]:
        left, right = right, left

    # Crop the eyes
    (x, y, w, h) = left
    left = cv2.equalizeHist(image[y:y+h, x:x+w])
    (x, y, w, h) = right
    right = cv2.equalizeHist(image[y:y+h, x:x+w])
    return left, right

def faceFromImage(image) -> Face:
    """
    Extracts the facial features from an image of a face.
    Its assumed that the image has been cropped to the face's region.
    """

    faceImage = cropFace(image)
    if faceImage is None:
        return None
    eyesImages = cropEyes(faceImage)
    if eyesImages is None:
        return None

    cv2.imshow("Face", faceImage)
    cv2.imshow("Left eye", eyesImages[0])
    cv2.imshow("Right eye", eyesImages[1])
    cv2.waitKey(1)

    face = Face()
    return face

def emotionFromImage(image) -> Emotion:
    """
    Extracts the emotion from an image of a face.
    Its assumed that the image has been cropped to the face's region.
    """
    emotion = Emotion.NEUTRAL
    # TODO: implement this
    return emotion
