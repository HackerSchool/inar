import sys

class Parser:
    """Parses options from the command line arguments."""

    def __init__(self):
        self.options = {}

    def add(self, name, description, default=None, parse=None):
        """
        Adds an option to the parser.
        Parsed options with no value will be set to True.
        """
        if parse is None:
            if isinstance(default, bool):
                parse = parseFlag
            elif isinstance(default, int):
                parse = parseInt
            else:
                parse = str

        self.options[name] = {
            "description": description,
            "default": default,
            "parse": parse,
        }
        pass

    def help(self):
        """Returns a help message listing the available options."""
        msg = "Options:\n"

        # Get the longest option name.
        longest_len = max([len(name) for name in self.options.keys()])

        for name, option in self.options.items():
            ws = " " * (longest_len - len(name))
            msg += f"  --{name}{ws}  {option['description']}"
            if option["default"] is not None:
                msg += f" (default: {option['default']})"
            msg += "\n"
        return msg

    def parse(self):
        """Parses the options added until now and returns their values."""
        values = {}
        for name, option in self.options.items():
            values[name] = option["default"]

        # Parse the command line arguments.
        previous = None
        for arg in (sys.argv[1:] + [""]):
            if arg.startswith("--") or arg == "":
                # Check if we were expecting a value for the previous option.
                if previous is not None:
                    if isinstance(self.options[previous]["default"], bool):
                        values[previous] = True
                    else:
                        print(f"Option --{previous} requires a value.")
                        previous = None
                        continue
                
                # Check if the option exists.
                if arg != "":
                    name = arg[2:]
                    if name in self.options:
                        previous = name
                    else:
                        print(f"Unknown option --{name}")
            elif previous is not None:
                # Parse the option's value.
                value = self.options[previous]["parse"](arg)
                if value is None:
                    print(f"Invalid value '{arg}' for --{previous}")
                else:
                    values[previous]
                previous = None
            else:
                print(f"Expected option, found '{arg}'")

        return values

def parseFlag(s):
    if s == "true" or s == "True":
        return True
    elif s == "false" or s == "False":
        return False

def parseInt(s):
    try:
        return int(s)
    except ValueError:
        return None
