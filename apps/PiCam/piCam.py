from picamera import PiCamera
import time
import datetime
import os
from apps.ImageService.imageService import ImageService

class PiCam:
    def __init__(self):
        self.camera = PiCamera()
        self.now = datetime.datetime.now()
        self.status = 'unset status'
   
    def take_picture(self):
        print('working')
        pass
        date = str(self.now)[:10]
        path = '/home/pi/images/'+ date 
        
        #add thing to queue 
        # send the picture to imageService at some point
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError:
                print ("Creation of the directory %s failed" % path)
            else:
                print ("Successfully created the directory %s " % path)

        fpath = '/home/pi/images/'+ date +'/' + str(time.time())[:-8] + '.jpg'
        file = open(fpath, 'wb')
        self.camera.capture(file)
        file.close()
        ImageService.appendImageQueue(fpath)
  
    def start_video(self):
        print('working')
        pass
#       file = open('/home/pi/images/' + str(time.time())[:-8] + '.h264', 'wb')
#       self.camera.start_recording(file)
    def stop_video(self):
        print('working')
        pass
#        self.camera.stop_recording()
#        file.close()
    
    def start_preview(self):
        print('working')
        pass
        
    def stop_preview(self):
        print('working')
        pass
        self.camera.stop_preview()

    def get_exposure_compensation(self):
        print('working')
        pass
        return self.camera.exposure_compensation

    def set_exposure_compensation(self, value):
        print('working')
        pass
        self.camera.exposure_compensation = value 
    
    def inc_exposure_compensation(self):
        print('working')
        pass
        self.camera.exposure_compensation+=5 
        
    def dec_exposure_compensation(self):
        print('working')
        pass
        self.camera.exposure_compensation-=5

    def get_shutter_speed(self):
        print('working')
        pass
        return self.camera.shutter_speed
    
    def set_sutter_speed(self, value):
        print('working')
        pass
        self.camera.shutter_speed = value    

    def inc_sutter_speed(self):
        print('working')
        pass
        self.camera.shutter_speed+=3
   
    def dec_sutter_speed(self):
        print('working')
        pass
        self.camera.shutter_speed-=3 

    def get_awb_mode(self):
        print('working')
        pass
        return self.camera.awb_mode
    
    def set_awb_mode(self, value):
        print('working')
        pass
        self.camera.awb_mode = value
    
    def get_awb_gains(self):
        print('working')
        pass
        return self.camera.awb_gains
    
    def set_awb_gains(self, value):
        print('working')
        pass
        self.camera.awb_gains = value

    def inc_awb_gains(self):
        print('working')
        pass
        self.camera.awb_gains+=0.2

    def dec_awb_gains(self):
        print('working')
        pass
        self.camera.awb_gains-=0.2 

    def get_iso(self):
        print('working')
        pass 
        return self.camera.iso    

    def set_iso(self, value):
        print('working')
        pass
        self.camera.iso = value

    def inc_iso(self):
        print('working')
        pass
        self.camera.iso += 100
    
    def dec_iso(self):
        print('working')
        pass
        self.camera.iso -= 100
    

# Export singleton
piCam = PiCam()

