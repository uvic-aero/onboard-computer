import socket
import time
import zlib
import cv2
import threading
from queue import Queue

class Connections:
    """Class for handling active connections"""

    def __init__(self, timeout):
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
        self.times_since_heartbeat[index] = time.time()

    # Clean up expired connections. Gets called everytime a new client connects, connections are cleaned.
    def cleanup_connections(self):
        i = 0
        while i < len(self.times_since_heartbeat):
            if(time.time() - self.times_since_heartbeat[i] > self.timeout):
                self.remove(i)
            i = i + 1
        return self.connections

    def update(self, address):
        if address in self.connections:
            self.read_heartbeat(address)
        else:
            self.add(address)

class VideoStream:
    """Class for streaming video. """
   # TODO: Write more complete docstring when distinction between classes is more clear.                                                                    

    def __init__(self):
        self.status = "down"
        self.port = 1201
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connections = Connections(4)

    def start(self):
        print("Starting VideoStream...")
        self.status = "running"
        self.listenThread()

    def stop(self):
        print("Stopping VideoStream...")
        self.status = "down"

    def send_frame(self, frame, address, quality=4):
        frame = encode_frame(frame)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.imencode('.jpg', grey, encode_param)[1].tostring()
        frame = zlib.compress(frame, -1)
        self.socket.sendto(frame, address)

    def listenThread(self):
        thread = threading.Thread(target = self.listen)
        thread.daemon = False
        thread.start()

    def listen(self, port=None):
        if port is None:
            port = self.port
        with threading.Lock():
            self.socket.bind(('', port))
        print('Listening on port', port)
        while True:
            self.connections.cleanup_connections()
            data, address = self.socket.recvfrom(3)
            data = data.decode('utf-8')
            if (data == "get"):
                self.connections.update(address)
            for address in self.connections.connections:
                print(address)

    def broadcast(self, frame):
        self.cleanup_connections()
        for address in self.connections.connections:
            self.send_frame(frame, address)

    # TODO: Add skeletons for additional class methods when functionality of class is made more clear.

videoStream = VideoStream()
