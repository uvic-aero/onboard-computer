import time
import datetime
import os

class PiCam:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.status = 'unset status'
   
    def take_picture(self):
        print('Camera Simulating Image Capture')

    def start_video(self):
        pass
    
    def stop_video(self):
        pass
    
    def start_preview(self):
        pass
    
    def stop_preview(self):
        pass

    def get_exposure_compensation(self):
        pass

    def set_exposure_compensation(self, value):
        pass
    
    def inc_exposure_compensation(self):
        pass
        
    def dec_exposure_compensation(self):
        pass

    def get_shutter_speed(self):
        pass
    
    def set_sutter_speed(self, value):
        pass
    
    def inc_sutter_speed(self):
        pass
   
    def dec_sutter_speed(self):
        pass

    def get_awb_mode(self):
        pass
    
    def set_awb_mode(self, value):
        pass
    
    def get_awb_gains(self):
        pass
    
    def set_awb_gains(self, value):
        pass

    def inc_awb_gains(self):
        pass

    def dec_awb_gains(self):
        pass

    def get_iso(self):
        pass 

    def set_iso(self, value):
        pass

    def inc_iso(self):
        pass
    
    def dec_iso(self):
        pass
    

# Export singleton
piCam = PiCam()

