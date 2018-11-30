import asyncio
from tornado import web
import datetime

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

