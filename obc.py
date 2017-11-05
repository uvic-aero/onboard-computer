import asyncio
import requests
import functools
import traceback
import time
from camera import camera
from api import API

groundstation_url = "127.0.0.1:4000"
onboardserver_url = "127.0.0.1:8000"

class OnboardComputer:
    def __init__(self):
        self.camera = camera
        self.api = API()

    async def run(self):
        print("Starting Onboard Computer")
        while self.camera.connected == False:
            await self.camera.check_and_start_connection()
        await self.camera.start_tasks()
        await self.api.start()



if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    obc = OnboardComputer()

    loop.run_until_complete(obc.run())
    loop.run_forever()
    loop.close()
