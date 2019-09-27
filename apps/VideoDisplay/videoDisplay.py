import asyncio
from tornado import web
from apps.PiCam.piCam import piCam


class VideoDisplay:
    def __init__(self):
        self.status = (
            "down"
        )  # this status is used to check if a service is functioning normaly or not
        # store class variables here.
        pass

    def start(self):
        print("starting videoDisplay")
        self.status = "running"
        # this function will at least initialize a window for the user to see the picam.
        pass

    def stop(self):
        print("stopping videoDisplay")
        self.status = "down"
        # this function should kill the camera viewing window and
        # any other processes it has started.
        pass

    def check_status(self):
        # check all possible processes that may not be working properly, make sure they return
        # expected values.
        # return list of broken services.
        pass

    def init_display(self):
        # open window with cam display
        pass

    # the following functions are designed to help with the process of recognizing infrared
    # intense light sources.

    def find_ir(self, frame):
        # would return a set of coordinates
        pass


videoDisplay = VideoDisplay()
