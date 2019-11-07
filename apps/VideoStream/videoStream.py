# Import Statements
import numpy as np
import socket
import cv2
import math
import threading
import zlib

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


    # TODO: Add skeletons for additional class methods when functionality of class is made more clear.
    def main_loop:
        keep_running = 1
        while keep_running:
            data, address = sock.recvfrom(4)
            data = data.decode('utf-8')
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
