from options import Parser
from robot import Robot
from protocol import Protocol
from constants import UPDATE_RATE

import cv2
import time

def run(options):
    """The main entry point for the controller."""

    robot = Robot()
    protocol = Protocol(not options["viewer"], not options["receiver"])

    if not options["single"]:
        # Setup connection.
        if options["ip"] is not None:
            protocol.connect(options["ip"], options["port"])
        else:
            protocol.listen(options["port"])
    elif options["receiver"] or options["viewer"]:
        raise RuntimeError("In single mode state and frames can't be received.")

    if not options["viewer"]:
        cap = cv2.VideoCapture(0)

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
                # TODO: apply preprocessing to the frame.
                # TODO: call the decision code depending on the mode (stalk, imitation, etc)
                # TODO: if necessary, mix the two states (imitation + predefined emotions)
                # TODO: update the robot target state.
                robot.update(1 / UPDATE_RATE)

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
