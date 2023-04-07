import pygame
import math
from state import Servo 
from constants import * 

LEFT_EYE_CENTER = (320,400)
RIGHT_EYE_CENTER = (480,400)

EYE_RADIUS = 50
PUPIL_RADIUS = 15

PUPIL_LIMIT = 30 # EYE_RADIUS - PUPIL_RADIUS - 5 Pixels, so the pupil is not in the limit of the eye

ANGLE_OF_STATE_UNIT = EYE_RADIUS / 180

Z_PLANE = 1000




def draw_eye(win,eye_x, eye_y, robot, position):
        # new_x, new_y = pygame.mouse.get_pos() # Gets mouse position

        #TODO: State needs to be initialized when the program runs, 
        # otherwhise it is not possible to run the scrip bellow


        robot_state =  robot.getActualState()
        # Checks which eye it is, and updates the new position of the pupil
        # This new position is based on the angle given to the servos of the
        # robot

        if position == "left":
            new_x =  robot_state.getPosition(Servo.L_EYE_X) * ANGLE_OF_STATE_UNIT * DIMENSION_X
            new_y =  robot_state.getPosition(Servo.L_EYE_Y) * ANGLE_OF_STATE_UNIT * DIMENSION_Y
        if position == "right":
            new_x =  robot_state.getPosition(Servo.R_EYE_X) * ANGLE_OF_STATE_UNIT
            new_y =  robot_state.getPosition(Servo.R_EYE_Y) * ANGLE_OF_STATE_UNIT
        else:
            print("Error, that eye does not exist")


        distance_x = new_x - eye_x
        distance_y = new_y - eye_y

        """"
            Angle between plane and line:

                            |u.n|
            sin(tetha) = ------------
                            |u|.|n|

            In our case n = (0,0,1) and u = (distance_x, distance_y, Z_PLANE)
            so |u.n| = uz.nz = Z_PLANE
            and
            |u|.|n| = |u|

        """
        #NOTE: It may seem that there is no plane on the mouse but that's 
        # because of the dimensions are small, so we cant add a great distance
        # to the mouse.

        norm_u = math.sqrt(distance_x**2 + distance_y**2 + Z_PLANE**2)
        calc_aux = Z_PLANE/norm_u
        theta = math.asin(calc_aux) # in radians
        true_distance = norm_u * math.cos(theta)

        distance = min(true_distance, PUPIL_LIMIT)

        angle = math.atan2(distance_y, distance_x) # angle for rotation
        pupil_x = eye_x + (math.cos(angle) * distance) # position of pupil of the eye in axis X
        pupil_y = eye_y + (math.sin(angle) * distance) # position of pupil of the eye in axis Y

        pygame.draw.circle(surface=win, center=(eye_x, eye_y), radius=EYE_RADIUS, color=(255, 255, 255)) # draw eye
        pygame.draw.circle(surface=win, center=(pupil_x, pupil_y), radius=PUPIL_RADIUS, color=(0, 255, 255)) # draw pupil

def draw_face(win,robot):
    pygame.draw.rect(surface=win, color=(255,229,204), rect= (250, 250, 300, 300) )  
    draw_eye(win,320, 400, robot, "left") # left eye
    draw_eye(win,480, 400, robot, "right") # right eye
