import asyncio
import requests
import functools
import socket
from http.client import HTTPResponse

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

groundstation_url = "127.0.0.1:4000"

socket.setdefaulttimeout(2) # 2 second timeout

class Camera:
    def __init__(self):
        self.connected = False
        self.location = ""

        self.connect()

    def connect(self):

        if self.connected == True:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        message = "\r\n".join([
            'M-SEARCH * HTTP/1.1',
            'HOST: 239.255.255.250:1900',
            'MAN: "ssdp:discover"',
            'ST: urn:schemas-sony-com:service:ScalarWebAPI:1',
            'MX: 1', ''])

        print(message)

        try:
            sock.sendto(message.encode(), ("239.255.255.250", 1900))
        except:
            print("Failed to query SSDP server")

        try:
            data = sock.recv(1024)

            response = HTTPResponse(data)
            response.begin()

            st = response.getheader('st')

            if st != 'urn:schemas-sony-com:service:ScalarWebAPI:1':
                return

            self.location = response.getheader('location')

            self.connected = True

        # Could not find the camera device
        except socket.timeout:
            return

        # Error while parsing http response
        except:
            return

class OnboardComputer:
    def __init__(self):
        self.camera = Camera()

    async def send_image(self):

        try:
            await asyncio.get_event_loop().run_in_executor(None, functools.partial(requests.post, '', timeout=5))
        except:
            pass

    async def run(self):

        while True:

            if self.camera.connected == False:
                self.camera.connect()
                continue

            

if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    loop.run_until_complete(OnboardComputer().run())

    loop.close()
