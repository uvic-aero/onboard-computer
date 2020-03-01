import socket
import cv2
import numpy as np
import sys
import zlib

class Client:

    def __init__(self):

	# Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = ('0.0.0.0', 1201) 

    def connect(self, address=None):

        if address != None: self.address = address

        while True:
            sent = self.sock.sendto("get".encode('utf-8'), self.address)
            data, server = self.sock.recvfrom(65507)
            if (data is not None):
                array = zlib.decompress(data, 0)
                array = np.frombuffer(array, dtype=np.dtype('uint8'))
                final = cv2.imdecode(array, 1)
                cv2.imshow("Image", final)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.disconnect() 
                    break

    def disconnect(self):
        self.sock.sendto("quit".encode('utf-8'), self.address)
        print("Asking the server to quit")
        self.sock.sendto("quit".encode('utf-8'), self.address)
        print("Quitting")
        cv2.destroyAllWindows()

videoClient = VideoClient()
