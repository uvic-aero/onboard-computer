import socket
import time
import zlib
import cv2

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
        return self.connections

class VideoStream:
    """Class for streaming video. """
   # TODO: Write more complete docstring when distinction between classes is more clear.

    def __init__(self):
        self.status = "down"
        self.port = 1201
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connections = Connections(3)

    def start(self):
        print("Starting VideoStream...")
        self.status = "running"

    def stop(self):
        print("Stopping VideoStream...")
        self.status = "down"

    def send_frame(self, frame): #Do not use, will be replaced with listen()
        data, address = self.socket.recvfrom(4)
        data = data.decode('utf-8')

        if (data == "get"):
            self.socket.sendto(frame, address)

    def compress_frame(self, frame, quality):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        encimg = cv2.imencode('.jpg', grey, encode_param)[1].tostring()
        encimg = zlib.compress(encimg, -1)
        videoStream.send_frame(encimg)

    def listen(self, port=self.port):
        self.socket.bind(('', port))
        while True:
            for connections in self.connections
                data, address = self.socket.recvfrom(4)
                if (data == "get"):
                    

    # TODO: Add skeletons for additional class methods when functionality of class is made more clear.
    

videoStream = VideoStream()