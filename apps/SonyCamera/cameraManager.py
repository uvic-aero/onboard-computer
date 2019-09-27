from .cameraAPI import CameraAPI, RecordMode
from http.client import HTTPResponse
from io import BytesIO

import xml.etree.ElementTree as ET
import netifaces
import requests
import socket
import time
from queue import Queue
from threading import Thread, Lock


__all__ = ["CameraManager"]

# TODO : Decide how to monitor connection and execute commands concurrently


class FakeSocket:
    def __init__(self, response_str):
        self._file = BytesIO(response_str)

    def makefile(self, *args, **kwargs):
        return self._file


class ConnHandler:
    # Class Field
    ssdp_req = "\r\n".join(
        [
            "M-SEARCH * HTTP/1.1",
            "HOST: 239.255.255.250:1900",
            'MAN: "ssdp:discover"',
            "ST: urn:schemas-sony-com:service:ScalarWebAPI:1",
            "MX: 1",
            "",
            "",
        ]
    )

    @staticmethod
    def scan_netifaces():
        """scan all network interface"""
        addresses = []
        for interface in netifaces.interfaces():
            links = netifaces.ifaddresses(interface)
            if netifaces.AF_INET not in links:
                continue
            for link in links[netifaces.AF_INET]:
                addresses.append(link["addr"])
        return addresses

    @staticmethod
    def get_camera_url(location):
        """Obtain camera url by parsing ssdp request"""
        # Parse SSDP get request as XML
        urn = "{urn:schemas-sony-com:av}"
        service = urn + "X_ScalarWebAPI_Service"
        service_type = urn + "X_ScalarWebAPI_ServiceType"
        action = urn + "X_ScalarWebAPI_ActionList_URL"

        root = ET.fromstring(requests.get(location).content)
        for service in root.iter(service):
            if service.find(service_type).text == "camera":
                camera_url = service.find(action).text + "/camera"
                return camera_url

    def get_sock_location(self, sock):
        message = self.ssdp_req
        try:
            sock.sendto(message.encode(), ("239.255.255.250", 1900))
            data = sock.recv(1024)
        except:
            print("Failed to query SSDP server.")
            return None

        res = HTTPResponse(FakeSocket(data))
        res.begin()

        st = res.getheader("st")
        if st != "urn:schemas-sony-com:service:ScalarWebAPI:1":
            return None
        else:
            location = res.getheader("location")
            return location


class CameraManager:
    def __init__(self):
        self.api = CameraAPI(manager=self)
        self.handler = ConnHandler()
        self.connected = False
        self.sock = socket.socket()
        self.thread = None
        self.run = True
        self.currentMode = RecordMode.NONE
        self.wantedMode = RecordMode.LIVE
        self.stillReceiver = None

    def start(self, stillReceiver):
        self.stillReceiver = stillReceiver
        self.run = True
        self.thread = Thread(target=self.loop)
        self.thread.start()

    def stop(self):
        print("Requesting Camera Manager stop")
        self.run = False

    def loop(self):
        while self.run:

            self.connected = self._check_connection()

            if self.connected:
                self.api._process_queue()
            else:
                time.sleep(1)
                self.currentMode = RecordMode.NONE
                print("Try to connect!")
                addresses = self.handler.scan_netifaces()
                for addr in addresses:
                    if self._connect(addr):
                        break

        print("Stopping Camera Manager")

    def _check_connection(self):
        url = self.api.url
        payload = self.api.payload
        payload["method"] = "startRecMode"
        try:
            res = requests.post(url, json=payload, timeout=1)
        except requests.exceptions.Timeout as ex:
            print("No connection : Wifi Connection problem.")
            return False
        except requests.exceptions.MissingSchema as ex:
            print("No connection : Invalid URL")
            return False
        except OSError as err:
            print("No connection : OS error, Failed to establish a new connection")
            return False
        except:
            print("No connection : Unknown error !")
            return False

        if res.status_code != 200:
            print("Bad request or camera server problem.")
            return False
        else:
            # self.api.start_record_mode()
            return True

    # TODO: Set appropriate timeouts
    def _connect(self, addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.settimeout(0.5)

        sock.bind((addr, 0))

        location = self.handler.get_sock_location(sock)
        if location is None:
            sock.close()
        else:
            camera_url = self.handler.get_camera_url(location)
            self.api._update_url(camera_url)
            self.api.start_record_mode()
            self.connected = True
            self.sock.close()
            self.sock = sock
            print("Connected ! Camera url: %s" % camera_url)


# This class is just for testing
# Without async module, Real test should have at least two threads
# One for check connection and execute command from the queue
# The other is for receiving orders and put it in the queue
class _ActiveObject:
    def __init__(self, cm):
        self.cm = cm

    def add_task(self, command):

        if not self.cm.connected:
            print("Drop the command : %s - No connection !" % command.__name__)
            return

        if self.cm.queue.full():
            print("Drop the command : %s - Queue is full !" % command.__name__)
        else:
            self.cm.queue.put(command)


if __name__ == "__main__":

    cm = CameraManager()
    cm.start()

    cm.api.check_status()

    cm.stop()

    """
	lock = Lock()

	cm = CameraManager()
	ao = _ActiveObject(cm)


	commands = [cm.api.still_capture, cm.api.zoom_in, cm.api.zoom_in, 
		cm.api.still_capture, cm.api.still_capture, cm.api.start_liveview,
		cm.api.zoom_out, cm.api.zoom_out, cm.api.still_capture, 
		cm.api.still_capture, cm.api.zoom_out, cm.api.stop_liveview,
		cm.api.stop_liveview, cm.api.still_capture, cm.api.zoom_in]

	def target_1():

		cm.start()

	def target_2():

		for command in commands:
			time.sleep(3)

			lock.acquire()
			ao.add_task(command)
			lock.release()


	thread_1 = Thread(target=target_1)
	thread_2 = Thread(target=target_2)

	print("Start the test !!! ")
	thread_1.start()
	thread_2.start()
	"""
