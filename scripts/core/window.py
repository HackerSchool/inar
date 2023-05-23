import pygame
import pygame_widgets
import math
#from state import Servo 
from constants import * 

from core import Robot, Debug

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# TODO: turn this into a class, move things from main


LEFT_EYE_CENTER = (320,400)
RIGHT_EYE_CENTER = (480,400)

EYE_RADIUS = 50
PUPIL_RADIUS = 15

PUPIL_LIMIT = 30 # EYE_RADIUS - PUPIL_RADIUS - 5 Pixels, so the pupil is not in the limit of the eye

ANGLE_OF_STATE_UNIT = EYE_RADIUS / 180

Z_PLANE = 1000


class Window:


    def __init__(self, x_dimension, y_dimension, _robot: Robot, _debug: Debug):
        self.isRunning = True

        self.debug = _debug
        self.robot= _robot
        self.win = pygame.display.set_mode((x_dimension,y_dimension))
        pygame.display.set_caption("INAR Simulator")

    def draw_eye(self, eye_x, eye_y, robot, position):
            new_x, new_y = pygame.mouse.get_pos() # Gets mouse position

            #TODO: State needs to be initialized when the program runs, 
            # otherwhise it is not possible to run the scrip bellow


            robot_state =  robot.getActualState()
            # Checks which eye it is, and updates the new position of the pupil
            # This new position is based on the angle given to the servos of the
            # robot
            """
            if position == "left":
                new_x =  robot_state.getPosition(Servo.L_EYE_X) * ANGLE_OF_STATE_UNIT * DIMENSION_X
                new_y =  robot_state.getPosition(Servo.L_EYE_Y) * ANGLE_OF_STATE_UNIT * DIMENSION_Y
            if position == "right":
                new_x =  robot_state.getPosition(Servo.R_EYE_X) * ANGLE_OF_STATE_UNIT * DIMENSION_X
                new_y =  robot_state.getPosition(Servo.R_EYE_Y) * ANGLE_OF_STATE_UNIT * DIMENSION_Y
            else:
                print("Error, that eye does not exist")
            """

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

            pygame.draw.circle(surface=self.win, center=(eye_x, eye_y), radius=EYE_RADIUS, color=(255, 255, 255)) # draw eye
            pygame.draw.circle(surface=self.win, center=(pupil_x, pupil_y), radius=PUPIL_RADIUS, color=(0, 255, 255)) # draw pupil

    def draw_face(self,robot):
        pygame.draw.rect(surface=self.win, color=(255,229,204), rect= (250, 250, 300, 300) )  
        self.draw_eye(320, 400, robot, "left") # left eye
        self.draw_eye(480, 400, robot, "right") # right eye

        pygame.draw.line(self.win, (0,0,0), (650, 0), (650, 800))
        pygame.display.flip()

        self.draw_text("Debug:", 32, 100)

    def draw_text(self, text, fontsize, y_position):
        # Initialize the font system and create the font and font renderer
        pygame.font.init()
        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, fontsize)
        # To create a surface containing `Some Text`
        label = font_renderer.render(
            text,   # The font to render
            1,             # With anti aliasing
            (0,0,0)) # RGB Color
        
        self.win.blit(label, (700,y_position))

    def draw_slider(self,uppperValue,downValue,step,y_position):
        slider = Slider(self.win, 700, y_position, 150, 10, min=downValue, max=uppperValue, step=step)

    def run(self):
        pygame.init()
        pygame.time.delay(100)

        # x_start, y_start, widht_dimension, radius_dimension,
        slider = Slider(self.win, 700, 0, 150, 10, min=0, max=5, step=1)

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print("Quitting... Sya :)")
                    self.isRunning = False

            if not self.isRunning:
                break
                
            self.win.fill((255,255,255))  # Fills with the colors inside
            
            self.draw_face(self.robot)
            
            pygame_widgets.update(events)
            
            if self.debug != "":
                for label in self.debug.all_labels():
                    self.draw_text(label["name"] + ": " + str(label["value"]) ,14, label["position"])
            
            
            pygame.display.update() 
         