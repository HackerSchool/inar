from options import Parser

def run(options):
    """The main entry point for the controller."""
    # TODO: init robot
    # TODO: main loop, update at the configured rate

if __name__ == "__main__":
    parser = Parser()
    parser.add("help", "Prints this help message.", default=False)
    parser.add("window", "Open debug window.", default=False)
    parser.add("servos", "Controls the servos.", default=False)
    parser.add("ip", "The IP address to connect to.")
    parser.add("port", "The port to listen/connect to.", default=10000)
    options = parser.parse()
    if options["help"]:
        print(parser.help())
    else:
        run(options)
