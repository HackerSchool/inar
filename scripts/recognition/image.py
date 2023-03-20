from .face import Face
from .emotion import Emotion

import cv2

def nothing(x):
    pass

faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
eyesCascade = cv2.CascadeClassifier('data/haarcascade_eye_tree_eyeglasses.xml')

blobParams = cv2.SimpleBlobDetector_Params()
blobParams.filterByArea = True
blobParams.maxArea = 1500
blobDetector = cv2.SimpleBlobDetector_create(blobParams)

cv2.namedWindow('face')
cv2.createTrackbar('threshold', 'face', 0, 255, nothing)

def cropFace(image):
    """
    Takes an image and returns a cropped image of the face.
    If no face is detected, None is returned.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return None

    # Pick the largest face
    largest = faces[0]
    for (x, y, w, h) in faces[1:]:
        if largest is None or w * h > largest[2] * largest[3]:
            largest = (x, y, w, h)

    # Crop the face
    (x, y, w, h) = largest
    return image[y:y+h, x:x+w]

def cropEyes(image):
    """
    Takes a cropped image of a face and returns two cropped images, one for each eye.
    Eyes on the left half of the image are considered the left eye, and vice versa.
    Eyes which are not detected are returned as None.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    eyes = eyesCascade.detectMultiScale(gray, 1.3, 5)
    width = image.shape[1]
    height = image.shape[0]

    left = None
    right = None

    # Pick the left and right eye
    for (x, y, w, h) in eyes:
        if y > height / 2:
            continue # Ignore eyes below the middle of the face

        center = (x + w / 2, y + h / 2)
        if center[0] < width / 2:
            left = image[y:y+h, x:x+w]
        else:
            right = image[y:y+h, x:x+w]

    return left, right

def findPupils(image, threshold):
    """
    Takes an image of an eye and returns the coordinates of the pupils.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    _, image = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Cut the eyebrows
    height, width = image.shape[:2]
    eyebrow_height = int(height / 5)

    # Erode and dilate to remove noise
    image = cv2.erode(image, None, iterations=2)
    image = cv2.dilate(image, None, iterations=4)
    image = cv2.medianBlur(image, 5)

    # Find the keypoints with blob detector
    return blobDetector.detect(image)

    

def faceFromImage(image) -> Face:
    """
    Extracts the facial features from an image of a face.
    Its assumed that the image has been cropped to the face's region.
    """

    faceImage = cropFace(image)
    if faceImage is None:
        return None
    eyesImages = cropEyes(faceImage)

    threshold = cv2.getTrackbarPos('threshold', 'face')

    for eyeImage in eyesImages:
        if eyeImage is None:
            continue

        keypoints = findPupils(eyeImage, threshold)
        cv2.drawKeypoints(eyeImage, keypoints, eyeImage, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow('face', image)
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
