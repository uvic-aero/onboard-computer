from picamera import PiCamera
import time
import datetime
import os

class PiCam:
    def __init__(self):
        self.camera = PiCamera()
        self.now = datetime.datetime.now()
        self.folder_not_created = True
   
    def take_picture(self):
        date = str(self.now)[:10]
        path = '/home/pi/images/'+ date 
        if self.folder_not_created:
            try:
                os.mkdir(path)
            except OSError:
                print ("Creation of the directory %s failed" % path)
            else:
                print ("Successfully created the directory %s " % path)

            self.folder_not_created = False

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
#
piCam = PiCam()

