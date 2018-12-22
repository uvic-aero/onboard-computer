from picamera import PiCamera
import time

class PiCam:
    def __init__(self):
        self.camera = PiCamera()
   
    def take_picture(self):
        file = open('/home/pi/images/' + str(time.time())[:-8] + '.jpg', 'wb')
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

