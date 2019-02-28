import asyncio
from tornado import web
import time
import os
import _thread
from apps.PiCam.piCam import piCam
from apps.PiCam.simulation.piCam import piCam as simulatedCamera

class Timelapse:
    interval = 3 #set default interval length.

    def __init__(self):
        self.status = 'Down'
        self.loop_flag = True
        self.camera = piCam
            
        
    def start(self):
        # Check if Simulation
        if os.environ.get('SIMULATE'):
            self.camera = simulatedCamera
            print('Setting simulated camera')

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
            self.camera.take_picture()
            time.sleep(self.interval) 

    def set_interval(self, newInterval):
        try:
            self.interval = newInterval
        except:
            print("invalid interval entered\n")

        pass

timelapse = Timelapse()



