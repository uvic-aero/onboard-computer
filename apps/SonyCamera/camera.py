import os
import socket
import asyncio
import traceback
import requests
import functools
from tornado import ioloop
from io import BytesIO
from http.client import HTTPResponse
from enum import Enum


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

socket.setdefaulttimeout(2) # 2 second timeout

class Status(Enum):
    Error = -1
    IDLE = 0
    NotReady = 1
    StillCapturing = 2
    StillSaving = 3
    ContentsTransfer = 4

class FakeSocket():
    def __init__(self, response_str):
        self._file = BytesIO(response_str)
    def makefile(self, *args, **kwargs):
        return self._file

class Camera:
    def __init__(self):
        self.connected = False
        self.location = ""
        self.status = Status.NotReady
        self.endpoint = ""
        self.params = {
            "id" : 1,
            "version" : '1.0',
            "params" : [],
            "method" : ""
        }
        self.liveview = None

    async def start_tasks(self):
        await self.zoom_in()
        await self.zoom_in()
        await self.zoom_out()
        await self.zoom_in()
        await self.take_picture()

    async def check_and_start_connection(self):
        if self.connected == True:
            print("Already connected")
            return True ###
        while self.connected == False:
            print('Starting connection to camera')
            while True :
                await asyncio.sleep(1)
                # Get IP addresses that match specific parameters
                for addr in [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)
                    if i[0] == socket.AF_INET and i[1] == socket.SOCK_DGRAM]:
                    # Attempt to find camera on this interface
                    found = await self.start_connection(addr)
                    if found is True:
                        print("Connection was established")
                        return True ###

    async def start_connection(self, addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.bind((addr, 0))
        # HTTP request
        message = "\r\n".join([
            'M-SEARCH * HTTP/1.1',
            'HOST: 239.255.255.250:1900',
            'MAN: "ssdp:discover"',
            'ST: urn:schemas-sony-com:service:ScalarWebAPI:1',
            'MX: 1', '', ''])
        print('Using interface %s' % addr)
        # Make sure the SSDP server is queried
        try:
            for _ in range(2):
                sock.sendto(message.encode(), ("239.255.255.250", 1900))   
        except:
            print("Failed to query SSDP server")

        try:
            data = sock.recv(1024)
            response = HTTPResponse(FakeSocket(data))
            response.begin()

            st = response.getheader('st')
            if st != 'urn:schemas-sony-com:service:ScalarWebAPI:1':
                return False

            self.location = response.getheader('location')
            print('Camera location header: %s' % self.location)
            
            await self.parse_ssdp_response()
            self.connected = True
            print('Connected to camera')

            return True


        except socket.timeout:
            print('Connection timed out')
            return False

        # Error while parsing http response
        except:
            traceback.print_exc()
            return False

    async def parse_ssdp_response(self):
        # Parse SSDP get request as XML
        root = ET.fromstring(requests.get(self.location).content)
        for service in root.iter('{urn:schemas-sony-com:av}X_ScalarWebAPI_Service'):
            if service.find("{urn:schemas-sony-com:av}X_ScalarWebAPI_ServiceType").text == "camera":
                self.endpoint = service.find("{urn:schemas-sony-com:av}X_ScalarWebAPI_ActionList_URL").text + "/camera"
        print("Camera endpoint: %s" % self.endpoint)

    async def send_command(self, method, param=None): 
        self.params["method"] = method
        self.params["params"] = [] if param is None else param

        try:
            res = await ioloop.IOLoop.instance().asyncio_loop.run_in_executor(None, functools.partial(requests.post, self.endpoint, json=self.params))
            if res.status_code != 200:
                raise Exception("Response status code: %s" % res.status_code)
            res_json = res.json()
            if "error" in res_json:
                raise Exception(res_json["error"][1]) ###
            return res_json
        except Exception as e:
            traceback.print_exc()
            return None

    async def check_camera_status(self):      
        res = await self.send_command("getEvent", [False]) ###
        return res["result"][1]['cameraStatus']

    async def camera_is_IDLE(self):
        status = await self.check_camera_status()
        isIDLE = (status == Status.IDLE.name)
        return isIDLE

    async def wait_camera_until_IDLE(self):
        while True:
            isIDLE = await self.camera_is_IDLE()
            if isIDLE:
                break

    async def take_picture(self):
        await self.wait_camera_until_IDLE()
        res = await self.send_command("actTakePicture")
        picture_url = res["result"][0][0]
        print("Picture url : ", picture_url)

        picture_name = picture_url.split("/")[-1]
        response = requests.get(picture_url)
        image = response.content

        pwd = os.path.dirname(__file__)
        folder_name = os.path.join(pwd,"picture")
        if not os.path.exists(folder_name):
            print ("Create the folder \"picture\".")
            os.mkdir(folder_name)

        picture_dir = os.path.join(folder_name, picture_name)
        with open(picture_dir, 'wb') as file:
            file.write(image)

    async def zoom_in(self):
        await self.wait_camera_until_IDLE()
        print ("Start Zoom In")
        await self.send_command("actZoom", ["in", "1shot"])
        print ("Complete Zoom In")

    async def zoom_out(self):
        await self.wait_camera_until_IDLE()
        print("Start Zoom Out")
        await self.send_command("actZoom", ["out", "1shot"])
        print("Complete Zoom out")

camera = Camera()
