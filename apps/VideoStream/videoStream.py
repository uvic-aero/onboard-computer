# Import Statements
import socket

class VideoStream:
    """Class for streaming video. """
   # TODO: Write more complete docstring when distinction between classes is more clear.

    def __init__(self):
        self.status = "down"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 1201))

    def start(self):
        print("Starting VideoStream...")
        self.status = "running"

    def stop(self):
        print("Stopping VideoStream...")
        self.status = "down"

    # TODO: Add skeletons for additional class methods when functionality of class is made more clear.
    

videoStream = VideoStream()
