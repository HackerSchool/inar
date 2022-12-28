from .robot import Robot

import struct
import pickle
import socket

class Protocol:
    """
    Holds the logic for communication between the robot and the computer
    connected to it.
    """

    def __init__(self, hasCamera, hasState):
        """
        If hasCamera is True, the protocol will send the camera image to the
        other side. Otherwise, it will expect the other side to send the camera
        image. The same logic applies to hasState.
        """
        self.hasCamera = hasCamera
        self.hasState = hasState

    def listen(self, port):
        """
        Listens for a connection on the specified port.
        """

        while True:
            # Get socket.
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((socket.gethostname(), port))
            print(f"Listening on {socket.gethostname()}:{port}")
            server.listen()
            (client, (ip, _)) = server.accept()
            self.socket = client
            print(f"Connection established with {ip}")

            # Check if we're compatible.
            self.sendBytes(struct.pack("??", self.hasCamera, self.hasState))
            (hasCamera, hasState) = struct.unpack("??", self.recvBytes(2))
            if hasCamera == self.hasCamera or hasState == self.hasState:
                print("Incompatible connection: both sides have the same role.")
                self.socket.close()
                self.socket = None
            else:
                break


    def connect(self, ip, port):
        """
        Connects to the specified IP address and port.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to {ip}:{port}")
        self.socket.connect((ip, port))
        print("Connection established")

        # Check if we're compatible.
        (hasCamera, hasState) = struct.unpack("??", self.recvBytes(2))
        self.sendBytes(struct.pack("??", self.hasCamera, self.hasState))

        if hasCamera and self.hasCamera:
            raise RuntimeError("Both sides supply cameras.")
        if not hasCamera and not self.hasCamera:
            raise RuntimeError("Neither side supplies a camera.")
        if hasState and self.hasState:
            raise RuntimeError("Both sides supply states.")
        if not hasState and not self.hasState:
            raise RuntimeError("Neither side supplies a state.")

    def update(self, robot: Robot):
        """
        Updates the robot's state and camera image, from data received, or
        sends the robot's state and camera image to the other side.
        """
        
        # If we don't have a camera, we expect the other side to send us a
        # frame.
        if self.hasCamera:
            self.send(robot.getFrame())
        else:
            robot.setFrame(self.recv())

        # If we don't have a state, we expect the other side to send us a
        # state.
        if self.hasState:
            self.send(robot.getActualState())
        else:
            robot.setActualState(self.recv())

    def send(self, obj):
        """
        Sends the specified object.
        """
        data = pickle.dumps(obj)
        header = struct.pack("!I", len(data))
        self.sendBytes(header)
        self.sendBytes(data)
    
    def recv(self):
        """
        Receives an object.
        """
        header = self.recvBytes(4)
        data = self.recvBytes(struct.unpack("!I", header)[0])
        return pickle.loads(data)

    def sendBytes(self, data):
        """
        Sends the specified data, with the specified length.
        """
        self.socket.sendall(data)

    def recvBytes(self, size):
        """
        Receives the specified number of bytes from the socket.
        """
        data = b""
        while len(data) < size:
            packet = self.socket.recv(size - len(data))
            if len(packet) == 0:
                raise RuntimeError("Connection closed.")
            data += packet
        return data