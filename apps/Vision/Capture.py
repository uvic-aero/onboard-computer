import cv2
import base64
import sys
import time
import importlib

if importlib.find_loader("picamera"):
    found_picamera = True
    from picamera import PiCamera
    from picamera.array import PiRGBArray
else:
    found_picamera = False

class Capture:
    def __init__(self):
        self.camera_feed = 0
        self.picamera = None
        if found_picamera:
            # initialize the camera and grab a reference to the raw camera capture
            self.picamera = PiCamera()
            self.picamera.resolution = (3280, 2464)
            self.picamera.framerate = 32
            rawCapture = PiRGBArray(self.picamera, size=(640, 480))
            self.camera_feed = camera.capture()
        pass

    def capture(self):
        cam = cv2.VideoCapture(self.camera_feed)
        ret_val, frame = cam.read()
        return cv2.imshow('my webcam', frame)

if __name__ == "__main__":
    print("kicking off video capture")
    capture = Capture()
    capture.capture()