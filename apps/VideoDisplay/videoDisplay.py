import asyncio
from tornado import web
from picamera import PiCamera

class VideoDisplay:
    def __init__(self):
        self.status = 'down' #this status is used to check if a service is functioning normaly or not
        self.camera = PiCamera()
        # store class variables here.
        pass
    def start(self):
        print('starting videoDisplay')
        self.status = 'running'
        # this function will at least initialize a window for the user to see the picam.
        pass

    def stop(self):
        print('stopping videoDisplay')
        self.status = 'down'
        self.camera.stop_preview()
        print('stopping videoDisplay')	
        # this function should kill the camera viewing window and 
        # any other processes it has started.
        pass

    def check_status(self):
        # check all possible processes that may not be working properly, make sure they return
        # expected values.
        # return list of broken services.
        pass

    def init_display(self):
        # open window with cam display
        pass

    # the following functions are designed to help with the process of recognizing infrared 
    # intense light sources.

    
    def find_ir(self, frame):
        #would return a set of coordinates 
        pass


videoDisplay = VideoDisplay()

class VideoDisplayStatus(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        try:
            self.write({
                'service':'videoDisplay',
                'status':videoDisplay.status})
            self.finish()
        except:
            print('Error Writing Request Response')
    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()



class VideoDisplayStop(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @web.asynchronous
    def get(self):  
        videoDisplay.stop()
        try:
            self.write({
                'service':'videoDisplay',
                'action':'Killing'})
            self.finish()
        except:
            print('Error Writing Request Response')
    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()



class VideoDisplayStart(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @web.asynchronous
    def get(self):  
        videoDisplay.start()
        try:
            self.write({
                'service':'videoDisplay',
                'action':'Starting'})
            self.finish()
        except:
            print('Error Writing Request Response')
    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()


