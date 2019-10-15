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
        pixhawk.start()


    def stop(self):
        print("Stopping Onboard Computer")

        # stop apps
        self.imageService.stop()
        self.timelapse.stop()
        self.pixhawk()


if __name__ == "__main__":
    obc = OnboardComputer()
    obc.start()
