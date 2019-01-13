#from picamera import PiCamera
import time
import datetime
import os

class PiCam:
    def __init__(self):
        #self.camera = PiCamera()
        self.now = datetime.datetime.now()
        self.status = 'unset status'
   
    def take_picture(self):
        pass
        date = str(self.now)[:10]
        path = '/home/pi/images/'+ date 
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError:
                print ("Creation of the directory %s failed" % path)
            else:
                print ("Successfully created the directory %s " % path)

        file = open('/home/pi/images/'+ date +'/' + str(time.time())[:-8] + '.jpg', 'wb')
        self.camera.capture(file)
        file.close()
#   
    def start_video(self):
        pass
#       file = open('/home/pi/images/' + str(time.time())[:-8] + '.h264', 'wb')
#       self.camera.start_recording(file)
    def stop_video(self, file):
        pass
#       self.camera.stop_recording()
#       file.close()
#   
    def start_preview(self):
        pass
        self.camera.start_preview()
    def stop_preview(self):
        pass
        self.camera.stop_preview()

# Export singleton
piCam = PiCam()

