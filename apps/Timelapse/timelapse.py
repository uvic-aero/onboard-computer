import asyncio
from tornado import web
import datetime
from picamera import PiCamera

class Timelapse:
    def __init__(self):
        self.status = 'Down'
        pass

    # The start and stop functions do not need to be used if the programmer 
    # thinks that this class should not take the form of a process

    def start(self):
        print('starting timelapse')
        #this function is responsible for inidtializing connections 
        #and processes that may be used by the ImageService class
        self.status = 'Running'
        print('starting timelapse')
        pass

    def stop(self):
        print('stopping timelapse')
        self.status = 'Down'
        print('stopping timelapse')
        pass


timelapse = Timelapse()

class TimelapseStatus(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @web.asynchronous
    def get(self):
        # Include when the last image was taken so that users can confirm 
        # this feature is working.
        try:
            self.write({
                'service':'Timelapse',
                'status':timelapse.status})
            self.finish()
        except:
            print('Error Writing Request Response')
    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()



class TimelapseStop(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @web.asynchronous
    def get(self):  
        timelapse.stop()
        try:
            self.write({
                'service':'timelapse',
                'action':'Killing'})
            self.finish()
        except:
            print('Error Writing Request Response')
 
    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()



class TimelapseStart(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @web.asynchronous
    def get(self):  
        timelapse.start()
        try:
            self.write({
                'service':'timelapse',
                'action':'Starting'})
            self.finish()
        except:
            print('Error Writing Request Response')
    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()


  
