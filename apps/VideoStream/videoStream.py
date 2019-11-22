# Import Statements
import numpy as np
import socket
import time

class Connections:
    """Class for handling active connections"""

    def ___init___(self, timeout):
        self.connections = []
        self.times_since_heartbeat = []
        self.timeout = timeout

    def add(self, new_address):
        self.connections.append(new_address)
        self.times_since_heartbeat.append(0)

    # Can remove by either address or index.
    def remove(self, to_remove):
        if(to_remove is str):
            to_remove = self.connections.index(to_remove)
        del self.connections[to_remove]
        del self.times_since_heartbeat[to_remove]

    def read_heartbeat(self, address):
        index = self.connections.index(address)
        times_since_heartbeat[index] = time.time()

    # Clean up expired connections.
    def cleanup_connections(self):
        i = 0
        while i < len(self.times_since_heartbeat):
            if(time.time() - self.times_since_heartbeat[i] > self.timeout):
                self.remove(i)
            i = i - 1

class VideoStream:

    """Class for streaming video. """
   # TODO: Write more complete docstring when distinction between classes is more clear.

    def __init__(self):
        self.status = "down"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 1201))
        self.compression_level = 6 

    def start(self):
        print("Starting VideoStream...")
        self.status = "running"

    def stop(self):
        print("Stopping VideoStream...")
        self.status = "down"

    def send_frame(self,frame):
        self.socket.sendto(frame[:1600], ('0.0.0.0', 12345))

videoStream = VideoStream()
