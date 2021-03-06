import socket
import time
import zlib
import cv2
import threading

class Connections:
    """Class for handling active connections"""

    def __init__(self, timeout):
        self.connections = {}
        self.timeout = timeout
        self.lock = threading.Lock()

    def add(self, new_address):
        key = new_address[0] + ':' + str(new_address[1])
        connection = {'socket':new_address, 'time':time.time()}
        self.connections[key] = connection

    def remove(self, to_remove):
        # if (to_remove is str):
        #     to_remove = self.connections.index(to_remove)
        del self.connections[to_remove]

    def cleanup(self):
        to_remove = []
        for key in self.connections.keys():
            if (time.time() - self.connections[key]['time'] > self.timeout):
                print("Client", key, "timed out.")
                to_remove.append(key)
        for key in to_remove:
            self.remove(key)

    def update(self, address):
        if address in self.connections:
            self.connections[address]['time'] = time.time()
        else:
            self.add(address)

class VideoStream:
    """Class for streaming video. """
    # TODO: Write more complete docstring when distinction between classes is more clear.                                                                    
    # TODO: Add skeletons for additional class methods when functionality of class is made more clear.
    
    def __init__(self):
        self.status = "down"
        self.port = 1201
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connections = Connections(2)
        self.socket.settimeout(2)

    def start(self):
        print("Starting VideoStream...")
        self.listen_thread()
        self.status = "running"

    def stop(self):
        print("Stopping VideoStream...")
        threading._shutdown()
        self.socket.close()
        self.status = "down"

    def send_frame(self, frame, address, quality=4):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.imencode('.jpg', grey, encode_param)[1].tostring()
        frame = zlib.compress(frame, -1)
        self.socket.sendto(frame, address)

    def listen_thread(self):
        listen = threading.Thread(target = self.listen)
        listen.start()

    def listen(self, port = None):
        if port is None:
            port = self.port
        self.socket.bind(('', port))
        print('Listening on port', port)
        while True:
            self.connections.lock.acquire()
            self.connections.cleanup()
            self.connections.lock.release()
            for key in self.connections.connections.keys():
                print(key)
            try:    
                data, address = self.socket.recvfrom(3)
                data = data.decode('utf-8')
                if (data == "get"):
                    self.connections.lock.acquire()
                    self.connections.update(address)
                    self.connections.lock.release()
            except socket.timeout:
                continue

    def broadcast(self, frame):
        for key in self.connections.connections.keys():
            self.send_frame(frame, self.connections.connections[key]['socket'])          

videoStream = VideoStream()
