import asyncio
import requests
import functools
import traceback
import time
from tornado import ioloop
from cameraManager import CameraManager
from api import API
from liveReceiver import LiveReceiver
groundstation_url = "127.0.0.1:4000"
onboardserver_url = "127.0.0.1:8000"

ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')

class OnboardComputer:
    def __init__(self):
        self.camera = camera
        self.api = API()

    async def run(self):
        print("Starting Onboard Computer")
        self.api.start()
        while self.camera.connected == False:
            await self.camera.check_and_start_connection()
        await self.camera.start_tasks()
        
if __name__ == '__main__':

    loop = ioloop.IOLoop.instance()
    native = loop.asyncio_loop
    obc = OnboardComputer()
    native.create_task(obc.run())
    loop.start()
