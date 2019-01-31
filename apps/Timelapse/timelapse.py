import asyncio
from tornado import web
import time
import _thread
from apps.PiCam.piCam import piCam

class Timelapse:
    interval = 3 #set default interval length.
    prevInterval = 3
    duration = 0
    photo_count = -1

    def __init__(self):
        self.status = 'Down'
        self.loop_flag = True
        self.stop_burst = False
        
    def start(self):
        self.loop_flag = True
        print('starting timelapse')
        self.status = 'Running'
        try:
            _thread.start_new_thread( self.start_timelapse, ( ))
        except:
            print('Failed to Create Timelapse Thread')
    
    def stop(self):
        print('stopping timelapse')
        self.status = 'Down'
        self.loop_flag = False

    def start_timelapse(self):
        self.photo_count = -1
        while self.loop_flag:
            
            time.sleep(float(self.interval)) # Sleep for 3 seconds
            
            if self.photo_count > 0:
                self.photo_count = self.photo_count - 1 
            if self.photo_count == 0:
                self.photo_count = self.photo_count - 1
                self.interval = self.prevInterval
                self.duration = 0
            # This loop is used to trigger a photo every X seconds, using piCam.take_picture().
            # My recomendation is to take a photo then use the 
            # time.sleep(seconds) function to pause the loop for a desired amount of time.
            pass
    
    def set_interval(self, newInterval):
        # This function is used to update the interval between each photo being taken.
        # Hint, update this class to store a variable called interval, 
        # then refer to that variable while inside the timelapse loop while sleeping.
        try:
            self.interval = newInterval
        except:
            print("invalid interval entered\n")

        pass

    def set_duration(self, newDuration, burstInterval):
        # take duration and new burst interval. for duration, take photos at burst interval.
        # return to previous interval after duration. include option to exit burst at any time. 
	# move variables to main class, count to current delay. new function to get interval + handlers
        try:
            self.duration = newDuration
            self.prevInterval = self.interval
            self.interval = burstInterval
            self.photo_count = float(self.duration) / float(self.interval)
        except:
            print("could not set new duration\n")

        pass

timelapse = Timelapse()



