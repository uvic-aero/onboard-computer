# Import Statements
import numpy as np
import socket
import cv2
import math
import threading

class VideoStream:
    """Class for streaming video. """
   # TODO: Write more complete docstring when distinction between classes is more clear.

    def __init__(self):
        self.status = "down"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 1201))
        
        self.cap = cv2.VideoCapture(0)
        
        #Configurations
        self.client_address = []
        self.port = 5100 
        self.img_length = 640 #New Resolution
        self.img_width = 640
        
        
    def start(self):
        print("Starting VideoStream...")
        self.status = "running"

    def stop(self):
        print("Stopping VideoStream...")
        self.status = "down"


    # TODO: Add skeletons for additional class methods when functionality of class is made more clear.
    def main_loop:
        while 1:
            data, address = sock.recvfrom(4)
            data = data.decode('utf-8')
            if(data=="get"):
                self.client_address.append(address)
            if(data=="close"): #If the desktop client closes we can get it to send a few times "close" in order for us to close
                self.client_address.remove() #-its connection and increase efficiency
            
    def buffer_frame(frame, self): 
        #frame is a numpy array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #TODO: Review what resolution (size) we want the image
        gray = cv2.resize(gray, (0, 0), fx=0.1, fy=0.1) 
        img = cv2.imencode('.jpg', gray)[1]
        buffer = img.toString()
        
        #compression
        
        
        

videoStream = VideoStream()        
