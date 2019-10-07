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
from apps.Config.config import config
from apps.Routes.routes import routes
from apps.ImageService.imageService import imageService
from apps.Timelapse.timelapse import timelapse
from apps.TelemData.telemData import telemData

class OnboardComputer:
    def __init__(self):
        self.routes = routes
        self.application = tornado.web.Application(self.routes)
        self.server = tornado.httpserver.HTTPServer(self.application)

    def start(self):
        print("Starting Onboard Computer")

        # start apps
        imageService.start()
        telemData.start()

        # start http server
        self.application.listen(config.values["obc"]["port"])
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        print("Stopping Onboard Computer")

        # stop apps
        self.imageService.stop()
        self.timelapse.stop()
        self.telemData()


if __name__ == "__main__":
    obc = OnboardComputer()
    obc.start()
