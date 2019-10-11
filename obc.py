# Dependencies
import asyncio
import argparse
import functools
import os
import signal
import requests
import traceback
import time

# import apps
from apps.Config.config import config
from apps.ImageService.imageService import imageService
from apps.Timelapse.timelapse import timelapse
from apps.Pixhawk.pixhawk import pixhawk

class OnboardComputer:
    def __init__(self):
        pass

    def start(self):
        print("Starting Onboard Computer")

        # start apps
        imageService.start()
<<<<<<< HEAD
        videoDisplay.start()
        pixhawk.start()
=======
        telemData.start()
>>>>>>> 4fc1f82be6b1373c222d146900e064766842638e



    def stop(self):
        print("Stopping Onboard Computer")

        # stop apps
        self.imageService.stop()
        self.timelapse.stop()
<<<<<<< HEAD
        self.videoDisplay.stop()
        self.pixhawk()
=======
        self.telemData()
>>>>>>> 4fc1f82be6b1373c222d146900e064766842638e


if __name__ == "__main__":
    obc = OnboardComputer()
    obc.start()
