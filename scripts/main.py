from core import Parser, Robot, Protocol, window
from constants import UPDATE_RATE
from control import MimicBehaviour

import pygame

import cv2
import time

def run(options):
    """The main entry point for the controller."""
    robot = Robot()
    protocol = Protocol(not options["viewer"], not options["receiver"])
    behaviour = MimicBehaviour()

    # TODO: allow changing the mode of the robot, e.g. using the protocol

    if not options["single"]:
        # Setup connection.
        if options["ip"] is not None:
            #protocol.connect(options["ip"], options["port"])
            pass
        else:
            #protocol.listen(options["port"])
            pass
    elif options["receiver"] or options["viewer"]:
        raise RuntimeError("In single mode state and frames can't be received.")

    if not options["viewer"]:
        cap = cv2.VideoCapture(0)

    if options["window"]:
        run = True
        pygame.init()

        win = pygame.display.set_mode((800,800))
        pygame.display.set_caption("INAR Simulator")

    # Then, run the main loop.
    start = time.time()
    acc = 0
    while True:
        # Calculate the time since the last update.
        now = time.time()
        acc += now - start
        start = now

        # Only update when enough time has passed.
        if acc >= 1 / UPDATE_RATE:
            acc -= 1 / UPDATE_RATE

            # If we're not receiving frames, capture one.
            if not options["viewer"]:
                success, frame = cap.read()
                if not success:
                    raise RuntimeError("Failed to capture frame.")
                robot.setFrame(frame)
            
            # Communicate with the other side if we're not in single mode.
            if not options["single"]:
                protocol.update(robot)

            # Update the robot state, if we're not receiving it.
            if not options["receiver"]:
                frame = robot.getFrame()
                robot.setTargetState(behaviour.update(robot))
                robot.update(1 / UPDATE_RATE)

            # Update servos
            if options["servos"]:
                pass # TODO: update the servos.

            if options["window"]:
                pygame.time.delay(100)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Quitting... Sya :)")
                        run = False

                if not run:
                    break
                win.fill((255,255,255))  # Fills with the colors inside
                window.draw_face(win, robot)
                pygame.display.update() 


if __name__ == "__main__":
    parser = Parser()
    parser.add("help", "Prints this help message.", default=False)
    parser.add("window", "Open debug window.", default=False)
    parser.add("servos", "Controls the servos.", default=False)
    parser.add("ip", "The IP address to connect to.")
    parser.add("port", "The port to listen/connect to.", default=10000)
    parser.add("receiver", "If set, will receive state instead of calculating it.", default=False)
    parser.add("viewer", "If set, will receive frames instead of capturing them.", default=False)
    parser.add("single", "If set, won't listen for connections.", default=False)
    options = parser.parse()
    if options["help"]:
        print(parser.help())
    else:
        run(options)
