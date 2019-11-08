# Import Statements
import numpy as np
import socket
import cv2
import math
import threading
import zlib
import sys

class VideoStream:

    """Class for streaming video. """
   # TODO: Write more complete docstring when distinction between classes is more clear.

    def __init__(self):
        self.status = "down"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 1201))

        self.cap = cv2.VideoCapture(0)

        #Configurations
        self.compression_level = 6 #default level of compression, we can turn it down for faster compression
        self.port = 5100
        self.img_length = 640 #New Resolution #Not used
        self.img_width = 640 #Not used


    def start(self):
        print("Starting VideoStream...")
        self.status = "running"

    def stop(self):
        print("Stopping VideoStream...")
        self.status = "down"

    def send_frame(self,frame):
        print(sys.getsizeof(frame))
        self.socket.sendto(frame[:1300], ('0.0.0.0', 3444))


    # TODO: Add skeletons for additional class methods when functionality of class is made more clear.
    def main_loop(self):
        keep_running = 1
        while keep_running:
            data, address = sock.recvfrom(4)
            data = data.decode('utf-8')
            if(data is None):
                continue
            if(data=="get"):
                buf = buffer_frame(self.cap.read())
                if len(buf) > 65507:
                    print("Image too large")
                    sock.sendto("FAIL".encode('utf-8'), address)
                    continue
                elif(data=="quit"):
                    keep_running = False
                socket.sendto(buf, address)
        print("Quitting...")
        sock.close()

    def buffer_frame(frame):
        #TODO: frame is a numpy array?
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #TODO: Review what resolution (size) we want the image, and create a configurable input
        gray = cv2.resize(gray, (0, 0), fx=0.1, fy=0.1)
        img = cv2.imencode('.jpg', gray)[1]
        buffer = img.toString()
        #compression
        buffer = zlib.compress(buffer, self.compression_level)
        return buffer



videoStream = VideoStream()

#######put in file test.py 
cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),1]
    encimg = cv2.imencode('.jpg', grey, encode_param)[1].tostring()
    print(sys.getsizeof(encimg))
    #frame = cv2.imdecode(encimg,1)
    videoStream.send_frame(encimg)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
videoStream.socket.close()
