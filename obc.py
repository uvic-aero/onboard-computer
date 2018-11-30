import asyncio
import requests
import functools
import traceback
import time
import signal
import tornado
from tornado import ioloop

from apps.ImageService.imageService import imageService, ImageServiceStatus
from apps.Timelapse.timelapse import timelapse, TimelapseStatus
from apps.VideoDisplay.videoDisplay import videoDisplay, VideoDisplayStatus

groundstation_url = "127.0.0.1:4000"
onboardserver_url = "127.0.0.1:8000"


class OnboardComputer:
    def __init__(self):
        self.routes = [
                (r"/status/imageService", ImageServiceStatus),
                (r"/status/timelapse", TimelapseStatus),
                (r"/status/videoDisplay", VideoDisplayStatus),
                ]

        self.application = tornado.web.Application(self.routes)
        self.server = tornado.httpserver.HTTPServer(self.application)
    
    def start(self, port):
        print("Starting Onboard Computer")
        
        #start apps
        imageService.start()
        timelapse.start()
        videoDisplay.start()

        #start http server
        self.application.listen(port) 
        tornado.ioloop.IOLoop.instance().start()
        



    def stop(self):
        print("Stopping Onboard Computer")

        #stop apps
        self.imageService.stop()
        self.imageService.stop()
        self.timelapse.stop()
        self.videoDisplay.stop()

if __name__ == '__main__':

    obc = OnboardComputer()
    obc.start(8000)


