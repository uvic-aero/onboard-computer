# from picamera import PiCamera
from apps.Pixhawk.pixhawk import pixhawk
from apps.ImageService.imageService import imageService
import time
import datetime
import os
import importlib
import uuid
import cv2
import numpy as np

if importlib.find_loader("picamera"):
    found_picamera = True
    from picamera import PiCamera
else:
    found_picamera = False


class PiCam:
    def __init__(self):
        self.camera = None
        if found_picamera:
            self.status = "PiCamera Connected"
            self.camera = cv2.VideoCapture(PiCamera())
        else:
            self.status = "PiCamera Not Connected"
            # for starting up local opencv capture
            self.camera = cv2.VideoCapture(0)
        self.now = datetime.datetime.now()
        self.counter = 0

    def capture(self):
        ret_val, frame = self.camera.read()
        return frame


# Export singleton
piCam = PiCam()
