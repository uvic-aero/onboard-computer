# Import Statements
import socket
import cv2
import zlib

class VideoStream:
    """Class for streaming video. """
   # TODO: Write more complete docstring when distinction between classes is more clear.

    def __init__(self):
        self.status = "down"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 1201))

    def start(self):
        print("Starting VideoStream...")
        self.status = "running"

    def stop(self):
        print("Stopping VideoStream...")
        self.status = "down"
    
    def send_frame(self, frame):
        data, address = self.socket.recvfrom(4)
        data = data.decode('utf-8')
        if (data == "get"):
            self.socket.sendto(frame, address)

    def compress_frame(self, frame, quality):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        encimg = cv2.imencode('.jpg', grey, encode_param)[1].tostring()
        encimg = zlib.compress(encimg, 5)
        videoStream.send_frame(encimg)

    # TODO: Add skeletons for additional class methods when functionality of class is made more clear.


videoStream = VideoStream()