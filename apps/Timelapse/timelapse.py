import asyncio
from tornado import web
import time
import _thread
from apps.PiCam.piCam import piCam

class Timelapse:
    interval = 3 #set default interval length.

    def __init__(self):
        self.status = 'Down'
        self.loop_flag = True
        self.camera = piCam
        
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
        while self.loop_flag:
            
            time.sleep(self.interval) # Sleep for 3 seconds
            self.camera.take_picture()
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

timelapse = Timelapse()



