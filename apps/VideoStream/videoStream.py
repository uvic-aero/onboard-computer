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

        #Configurations
        self.client_address = "0.0.0.0"
        self.img_length = 640 #New Resolution
        self.img_width = 640

    def start(self):
        print("Starting VideoStream...")
        self.status = "running"

    def stop(self):
        print("Stopping VideoStream...")
        self.status = "down"


    # TODO: Add skeletons for additional class methods when functionality of class is made more clear.


    def send_data(chunk):
        socket.sendTo(chunk, self.client_address)

    def buffer_frame(frame, self): #make 4 threads for 4 chunks, each thread sending its corresponding chunk
        #frame is a numpy array

        img = cv2.imencode('.jpg', frame)[1]
        img.resize(img, (self.img_length, self.img_width))
        buffer = img.toString()
        quarter_buffer_length = (len(buffer)/4)
        quarter_buffer_length= math.floor(quarter_buffer_length)

        chunk1 = buffer[0:quarter_buffer_length]
        chunk2 = buffer[quarter_buffer_length:quarter_buffer_length*2]
        chunk3 = buffer[quarter_buffer_length*2:quarter_buffer_length*3]
        chunk4 = buffer[quarter_buffer_length*3:(len(buffer))]

        t1 = threading.Thread(target=send_data, args=chunk1)
        t2 = threading.Thread(target=send_data, args=chunk2)
        t3 = threading.Thread(target=send_data, args=chunk3)
        t4 = threading.Thread(target=send_data, args=chunk4)

        t1.start()   #sends 4 chunks via 4 threads
        t2.start()
        t3.start()
        t4.start()
        

videoStream = VideoStream()        
