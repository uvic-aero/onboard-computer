# Dependencies
import asyncio
import argparse
import functools
import os
import signal
import requests
import traceback
import time
import tornado
from tornado import ioloop

# import apps
from apps.Routes.routes import routes
from apps.ImageService.imageService import imageService
from apps.VideoDisplay.videoDisplay import videoDisplay
from apps.Timelapse.timelapse import timelapse

groundstation_url = "127.0.0.1:4000"
onboardserver_url = "127.0.0.1:8000"


class OnboardComputer:
    def __init__(self):
        self.routes = routes
        self.application = tornado.web.Application(self.routes)
        self.server = tornado.httpserver.HTTPServer(self.application)
        self.get_arguments() 

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

    def get_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--simulate", "-s", nargs='?', dest='simulate',
                        const=True, default=False,
                        help="Activate Simulation Mode")
        args = parser.parse_args()
        
        if args.simulate:
            print('setting env var')
            os.environ["SIMULATE"] = 'SIMULATING'

if __name__ == '__main__':

    obc = OnboardComputer()
    obc.start(1600)


