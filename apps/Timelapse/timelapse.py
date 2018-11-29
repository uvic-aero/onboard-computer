<<<<<<< HEAD
import asyncio
from tornado import web

class Timelapse:
    def __init__(self):
        pass

    # The start and stop functions do not need to be used if the programmer 
    # thinks that this class should not take the form of a process

    def start(self):
        #this function is responsible for inidtializing connections 
        #and processes that may be used by the ImageService class
        pass

    def stop(self):
        pass

class TimelapseStatus(web.RequestHandler):
    @web.asynchronous
    def get(self):
        try:
            self.write({
                'service':'Timelapse',
                'status':'broken'})
            self.finish()
        except:
            print('Error Writing Request Response')
=======
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
>>>>>>> 26167a4266af14726ad3507bbdc3c9edecb40707
