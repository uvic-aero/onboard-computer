import asyncio
import time
import os
import _thread
from apps.Config.config import config
from apps.PiCam.piCam import piCam
from apps.PiCam.simulation.piCam import piCam as simulatedCamera


class Timelapse:
    def __init__(self):
        self.status = "Down"
        self.loop_flag = True
        self.camera = piCam
        self.stop_burst = False

        # set default interval length.
        self.interval = config.values["timelapse"]["interval"]
        self.prev_interval = 3
        self.duration = 0
        self.photo_count = -1

    # Start the timelapse application
    def start(self):
        # Check if Simulation
        if os.environ.get("SIMULATE"):
            self.camera = simulatedCamera

        self.loop_flag = True
        print("starting timelapse")
        self.status = "Running"
        try:
            _thread.start_new_thread(self.start_timelapse, ())
        except:
            print("Failed to Create Timelapse Thread")

    # Stop the timelapse application
    def stop(self):
        print("stopping timelapse")
        self.status = "Down"
        self.loop_flag = False

    # Run a loop that takes photos every X seconds
    def start_timelapse(self):
        self.photo_count = -1
        while self.loop_flag:
            self.camera.take_picture()
            time.sleep(float(self.interval))  # Sleep for 3 seconds
            # If Duration set, decrease photo count
            if self.photo_count > 0:
                self.photo_count = self.photo_count - 1
            if self.photo_count == 0:
                self.photo_count = self.photo_count - 1
                self.interval = self.prev_interval
                self.duration = 0

    # Update the interval between photos being taken
    def set_interval(self, newInterval):
        try:
            self.interval = newInterval
        except:
            print("invalid interval entered\n")

        pass

    # For a given amount of time ( new_duration ), photos
    # will be captured with a temporary interval ( burst_interval )
    def set_duration(self, new_duration, burst_interval):
        try:
            self.duration = new_duration
            self.prev_interval = self.interval
            self.interval = burst_interval
            self.photo_count = float(self.duration) / float(self.interval)
        except:
            print("could not set new duration\n")

        pass


timelapse = Timelapse()
