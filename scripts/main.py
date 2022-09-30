from options import Parser
from robot import Robot
from constants import UPDATE_RATE
import time

def run(options):
    """The main entry point for the controller."""

    robot = Robot()

    if not options["single"]:
        # Setup connection.
        if options["ip"] is not None:
            robot.connect(options["ip"], options["port"])
        else:
            robot.listen(options["port"])
    elif options["receiver"]:
        raise RuntimeError("Cannot receive in single mode.")

    # Then, run the main loop.
    start = time.time()
    acc = 0
    while True:
        # Calculate the time since the last update.
        now = time.time()
        acc += now - start
        start = now

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

if __name__ == "__main__":
    parser = Parser()
    parser.add("help", "Prints this help message.", default=False)
    parser.add("window", "Open debug window.", default=False)
    parser.add("servos", "Controls the servos.", default=False)
    parser.add("ip", "The IP address to connect to.")
    parser.add("port", "The port to listen/connect to.", default=10000)
    parser.add("receiver", "If set, will receive state instead of sending.", default=False)
    parser.add("single", "If set, won't listen for connections.", default=False)
    options = parser.parse()
    if options["help"]:
        print(parser.help())
    else:
        run(options)
