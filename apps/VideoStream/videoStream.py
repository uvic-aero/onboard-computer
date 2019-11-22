# Import Statements
import numpy as np
import socket

class VideoStream:

    """Class for streaming video. """
   # TODO: Write more complete docstring when distinction between classes is more clear.

    def __init__(self):
        self.status = "down"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 1201))
        self.compression_level = 6 #default level of compression, we can turn it down for faster compression
        self.port = 5100

    def start(self):
        print("Starting VideoStream...")
        self.status = "running"

    def stop(self):
        print("Stopping VideoStream...")
        self.status = "down"

    def send_frame(self,frame):
        self.socket.sendto(frame[:1600], ('0.0.0.0', 12345))

videoStream = VideoStream()
