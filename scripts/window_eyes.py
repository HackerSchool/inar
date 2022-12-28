import pygame
import math

def draw_eye(win,eye_x, eye_y):
        mouse_x, mouse_y = pygame.mouse.get_pos() # Gets mouse position

        distance_x = mouse_x - eye_x
        distance_y = mouse_y - eye_y
        distance = min(math.sqrt(distance_x**2 + distance_y**2), 30)
        angle = math.atan2(distance_y, distance_x) # angle for rotation

        pupil_x = eye_x + (math.cos(angle) * distance) # position of pupil of the eye in axis X
        pupil_y = eye_y + (math.sin(angle) * distance) # position of pupil of the eye in axis Y

        pygame.draw.circle(surface=win, center=(eye_x, eye_y), radius=50, color=(255, 255, 255)) # draw eye
        pygame.draw.circle(surface=win, center=(pupil_x, pupil_y), radius=15, color=(0, 255, 255)) # draw pupil

def draw_face(win):
    pygame.draw.rect(surface=win, color=(255,229,204), rect= (250, 250, 300, 300) )  
    draw_eye(win,320, 400) # left eye
    draw_eye(win,480, 400) # right eye


if __name__ == '__main__':
    pygame.init()

    win = pygame.display.set_mode((800,800))
    pygame.display.set_caption("INAR Simulator")

    run = True

    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        win.fill((255,255,255))  # Fills with the colors inside
        draw_face(win)
        pygame.display.update() 
        
    pygame.quit()