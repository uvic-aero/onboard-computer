import asyncio
import requests
import functools
import traceback
import time
from camera import Camera

groundstation_url = "127.0.0.1:4000"

class OnboardComputer:
    def __init__(self):
        self.camera = Camera()

    async def send_image(self):

        try:
            await asyncio.get_event_loop().run_in_executor(None, functools.partial(requests.post, '', timeout=5))
        except:
            pass

    async def run(self):

        print("Starting Onboard Computer")

        while self.camera.connected == False:
            await asyncio.sleep(1)
            await self.camera.connect()

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    obc = OnboardComputer()

    loop.run_until_complete(obc.run())

    loop.run_forever()

    loop.close()
