import asyncio
import requests
import functools
import traceback
import time
import signal
from tornado import ioloop
from cameraManager import CameraManager
from api import API
from liveReceiver import LiveReceiver
from stillReceiver import StillReceiver

ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')

class OnboardComputer:
    def __init__(self):
        self.cameraManager = CameraManager()
        self.api = API(self.cameraManager)
        self.stillReceiver = StillReceiver(self.cameraManager)
        self.liveReceiver = LiveReceiver(self.cameraManager)

    async def run(self):
        print("Starting Onboard Computer")
        self.api.start()
        self.cameraManager.start(self.stillReceiver)
        self.stillReceiver.start()
        self.liveReceiver.start()

    def stop(self):
        print("Stopping Onboard Computer")
        self.liveReceiver.stop()
        self.stillReceiver.stop()
        self.cameraManager.stop()

if __name__ == '__main__':

    loop = ioloop.IOLoop.instance()
    native = loop.asyncio_loop

    def signal_handler(*args):
        # A SIGINT is a request for the application to stop; kill the event loop
        loop.add_callback_from_signal(loop.stop)

    # An empty function is enough to wake up event loop so interrupts can be handled
    def check_should_exit():
        pass

    # Start OBC + async tasks
    obc = OnboardComputer()
    native.create_task(obc.run())

    # Capture crl+c
    signal.signal(signal.SIGINT, signal_handler)

    # Force IOLoop to wake up so interrupts can be handled
    ioloop.PeriodicCallback(check_should_exit, 100).start()

    # Enter event loop
    loop.start()

    # Shutdown code
    obc.stop()
