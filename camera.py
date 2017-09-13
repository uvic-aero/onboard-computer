import socket
import asyncio
import netifaces
import traceback
import requests
import functools
from io import BytesIO
from http.client import HTTPResponse
from enum import Enum
from liveview import Liveview

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

socket.setdefaulttimeout(2) # 2 second timeout

class Status(Enum):
    Error = -1
    Idle = 0
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
            "id": 1,
            "version": "1.0",
            "params": [],
            "method": ""
        }
        self.liveview = None

    async def connect(self):

        if self.connected == True:
            return

        print('Starting connection to camera')

        for interface in netifaces.interfaces():

            links = netifaces.ifaddresses(interface)

            if netifaces.AF_INET not in links:
                continue

            for link in links[netifaces.AF_INET]:
            
                found = await self.send_discovery(link['addr'])

                if found is True:
                    return

    async def send_discovery(self, addr):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.bind((addr, 0))

        message = "\r\n".join([
            'M-SEARCH * HTTP/1.1',
            'HOST: 239.255.255.250:1900',
            'MAN: "ssdp:discover"',
            'ST: urn:schemas-sony-com:service:ScalarWebAPI:1',
            'MX: 1', '', ''])

        print('Using interface %s' % addr)
        
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

            await self.set_record_mode()
            #self.update_camera_status()
            await self.start_liveview()

            return True

        # Could not find the camera device
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
        self.params["params"] = [] if param is None else [param]

        try:
            print(self.params)
            res = await asyncio.get_event_loop().run_in_executor(None, functools.partial(requests.post, self.endpoint, json=self.params))

            if res.status_code != 200:
                raise Exception("Response status code: %s" % res.status_code)

            res_json = res.json()

            # API errors are returned as [code, message] so pull out the message
            if "error" in res_json:
                raise Exception(res_json["error"][1])

            return res_json
        except Exception as e:
            traceback.print_exc()
            return None

    async def set_record_mode(self):
        
        await self.send_command("startRecMode")
        print("Camera entering recMode")

    async def update_camera_status(self):
        
        await self.send_command("getEvent", True)

    async def take_picture(self):

        await self.send_command("actTakePicture")

    async def start_liveview(self):
        
        res = await self.send_command("startLiveview")
        liveview_url = res['result'][0]

        print("Liveview URL: %s" % liveview_url)

        self.liveview = Liveview(liveview_url)
        await self.liveview.start()
