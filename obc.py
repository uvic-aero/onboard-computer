import asyncio
import requests
import functools
import traceback
import time
import signal
import tornado
from tornado import ioloop

from apps.ImageService.imageService import ImageService, ImageServiceStatus

groundstation_url = "127.0.0.1:4000"
onboardserver_url = "127.0.0.1:8000"


class OnboardComputer:
    def __init__(self):

        self.imageService = ImageService()

        self.routes = [
                (r"/status/imageService", ImageServiceStatus)
                ]

        self.application = tornado.web.Application(self.routes)
        self.server = tornado.httpserver.HTTPServer(self.application)
    
    def start(self, port):
        print("Starting Onboard Computer")
        

        #start http server
        self.application.listen(port) 
        tornado.ioloop.IOLoop.instance().start()
        



    def stop(self):
        print("Stopping Onboard Computer")

if __name__ == '__main__':

    obc = OnboardComputer()
    obc.start(8000)


