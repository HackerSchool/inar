from state import State
import socket
import pickle
import struct

class Robot:
    """
    Represents the robot's hardware and abstracts away the details of
    controlling it.
    """
    def __init__(self):
        self.state = State()
        self.frame = None
        self.socket = None

        # Initial target state.
        self.lookAt((0, 0, 10))

    def lookAt(self, point):
        """
        Sets the desired point to look at.
        The coordinate system of the point is such that X is right, Y is up, Z
        is forward. One unit is equal to the distance between the eyes' centers.
        The position between the eyes is (0, 0, 0).
        """
        self.lookAtTarget = point

    def update(self, deltaT):
        """
        Updates the robot's state taking into account the time that has passed
        since the last update.
        """
        pass

    def listen(self, port):
        """Accepts a connection on the given port. Blocks until established."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), port))
        print(f"Listening on {socket.gethostname()}:{port}")
        server.listen()
        (client, (ip, _)) = server.accept()
        self.socket = client
        print(f"Connection established with {ip}")

    def connect(self, ip, port):
        """Connects to the given IP address and port."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to {ip}:{port}")
        self.socket.connect((ip, port))
        print("Connection established")

    def receive(self):
        """Receives the new state from the connection."""

        # Receive the header.
        header = b""
        while len(header) < 4:
            packet = self.socket.recv(4 - len(header))
            if len(packet) == 0:
                raise RuntimeError("Connection closed.")
            header += packet
        length = struct.unpack("!I", header)[0]

        # Then receive the data.
        data = b""
        while len(data) < length:
            packet = self.socket.recv(length - len(data))
            if len(packet) == 0:
                raise RuntimeError("Connection closed.")
            data += packet

        # Unpickle the data.
        self.state = pickle.loads(data)

    def send(self):
        """Sends the state to the connection."""

        # Pickle the data, create header.
        data = pickle.dumps(self.state)
        header = struct.pack("!I", len(data))

        # Send the header and then the data.
        self.socket.sendall(header)
        self.socket.sendall(data)

    def getState(self):
        """Returns the current state of the robot."""
        return self.state

    def getFrame(self):
        """Returns the last frame captured by the robot's camera."""
        return self.frame
