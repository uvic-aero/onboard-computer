from picamera import PiCamera
import time

class PiCam:
    self.camera = PiCamera()
    
    def take_picture(self):
        file = open('/home/pi/images' + str(time.time())[:-8] + '.jpg', 'wb')
        self.camera.capture(file)
        file.close()
    
    def start_video(self):
        file = open('/home/pi/images' + str(time.time())[:-8] + '.h264', 'wb')
        self.camera.start_recording(file)
    def stop_video(self, file):
        self.camera.stop_recording()
        file.close()
    
    def start_preview(self):
        self.camera.start_preview()
    def stop_preview(self):
        self.camera.stop_preview()

piCam = PiCam()
