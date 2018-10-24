import datetime
from camera import camera

isRunning = False;

class Timelapse:

    def __init__(self):
        isRunning = False

    def start(self):
        isRunning = True
        self.run()

    def stop(self):
        isRunning = False

    def run(self):
        while isRunning:
            if (datetime.now().strftime('%S')) % 3 == 0:
                camera.take_picture()
