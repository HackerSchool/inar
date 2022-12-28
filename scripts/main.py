<<<<<<< HEAD
from options import Parser
from robot import Robot
from constants import UPDATE_RATE
=======
from core import Parser, Robot, Protocol
from constants import UPDATE_RATE
from control import MimicBehaviour

import cv2
>>>>>>> d3c205392f024ac82a0499164e270e1de38c0cdf
import time

def run(options):
    """The main entry point for the controller."""

    robot = Robot()
<<<<<<< HEAD
=======
    protocol = Protocol(not options["viewer"], not options["receiver"])
    behaviour = MimicBehaviour()

    # TODO: allow changing the mode of the robot, e.g. using the protocol
>>>>>>> d3c205392f024ac82a0499164e270e1de38c0cdf

    if not options["single"]:
        # Setup connection.
        if options["ip"] is not None:
<<<<<<< HEAD
            robot.connect(options["ip"], options["port"])
        else:
            robot.listen(options["port"])
    elif options["receiver"]:
        raise RuntimeError("Cannot receive in single mode.")
=======
            protocol.connect(options["ip"], options["port"])
        else:
            protocol.listen(options["port"])
    elif options["receiver"] or options["viewer"]:
        raise RuntimeError("In single mode state and frames can't be received.")

    if not options["viewer"]:
        cap = cv2.VideoCapture(0)
>>>>>>> d3c205392f024ac82a0499164e270e1de38c0cdf

    # Then, run the main loop.
    start = time.time()
    acc = 0
    while True:
        # Calculate the time since the last update.
        now = time.time()
        acc += now - start
        start = now

<<<<<<< HEAD
        # If we are the receiver, receive the new state.
        # Otherwise, if enough time has passed, update the state.
        if options["receiver"]:
            robot.receive()
        elif acc >= 1 / UPDATE_RATE:
            acc -= 1 / UPDATE_RATE

            robot.update(1 / UPDATE_RATE)
            
            # Send the new state to the receiver, if any.
            if not options["single"]:
                robot.send()
=======
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
>>>>>>> d3c205392f024ac82a0499164e270e1de38c0cdf

if __name__ == "__main__":
    parser = Parser()
    parser.add("help", "Prints this help message.", default=False)
    parser.add("window", "Open debug window.", default=False)
    parser.add("servos", "Controls the servos.", default=False)
    parser.add("ip", "The IP address to connect to.")
    parser.add("port", "The port to listen/connect to.", default=10000)
<<<<<<< HEAD
    parser.add("receiver", "If set, will receive state instead of sending.", default=False)
=======
    parser.add("receiver", "If set, will receive state instead of calculating it.", default=False)
    parser.add("viewer", "If set, will receive frames instead of capturing them.", default=False)
>>>>>>> d3c205392f024ac82a0499164e270e1de38c0cdf
    parser.add("single", "If set, won't listen for connections.", default=False)
    options = parser.parse()
    if options["help"]:
        print(parser.help())
    else:
        run(options)
