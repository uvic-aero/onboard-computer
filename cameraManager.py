from cameraAPI import CameraAPI
from http.client import HTTPResponse
from io import BytesIO

import xml.etree.ElementTree as ET
import netifaces
import requests
import socket
import time
from  queue import Queue
from threading import Thread, Lock


__all__ = ['CameraManager']

# TODO : Decide how to monitor connection and execute commands concurrently

class FakeSocket:
	def __init__(self, response_str):
		self._file = BytesIO(response_str)
	def makefile(self, *args, **kwargs):
		return self._file

class ConnHandler():
	# Class Field
	ssdp_req = "\r\n".join([
			'M-SEARCH * HTTP/1.1',
			'HOST: 239.255.255.250:1900',
			'MAN: "ssdp:discover"',
			'ST: urn:schemas-sony-com:service:ScalarWebAPI:1',
			'MX: 1', '', ''])

	@staticmethod
	def scan_netifaces():
		"""scan all network interface"""
		addresses = []
		for interface in netifaces.interfaces():
			links = netifaces.ifaddresses(interface)
			if netifaces.AF_INET not in links:
				continue
			for link in links[netifaces.AF_INET]:
				addresses.append(link['addr'])
		return addresses

	@staticmethod
	def get_camera_url(location):
		"""Obtain camera url by parsing ssdp request"""
        # Parse SSDP get request as XML
		urn = '{urn:schemas-sony-com:av}'
		service = urn + 'X_ScalarWebAPI_Service'
		service_type = urn + 'X_ScalarWebAPI_ServiceType'
		action = urn + 'X_ScalarWebAPI_ActionList_URL'
		
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
			print("Failed to query SSDP server")
			return None

		res = HTTPResponse(FakeSocket(data))
		res.begin()
		
		st = res.getheader('st')
		if st != 'urn:schemas-sony-com:service:ScalarWebAPI:1':
			return None
		else:
			location = res.getheader('location')
			return location

class CameraManager:

	def __init__(self):
		self.api = CameraAPI()
		self.handler = ConnHandler()
		self.connected = False
		self.sock = socket.socket()
		self.queue = Queue(20)

	# TODO
	def start(self):
		while True:
			self.connected = self._check_connection()
			if self.connected:
				print("Sock works")
				if not self.queue.empty():
					command = self.queue.get()
					command()
				
			
			else:
				print("Try to reconnect!")
				addresses = self.handler.scan_netifaces()
				for addr in addresses:
					if self._connect(addr):
						break
				time.sleep(0.5)

	def _check_connection(self):
		url = self.api.url
		payload = self.api.payload
		payload['method'] = 'startRecMode'
		try:  
			res = requests.post(url, json=payload, timeout=0.5)
		except requests.exceptions.Timeout as ex:
			print("Server doesn't respond.")
			return False
		except requests.exceptions.MissingSchema as ex:
			print("Invalid URL")
			return False
		except OSError as err:
			print("OS error: {0}".format(err))
			return False
		except:
			pass

		if res.status_code != 200:
			print("Status code : ",res.status_code)
			return False
		else:
			self.api.start_record_mode()
			return True

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
			self.api.update_url(camera_url)
			self.connected = True
			self.sock.close()
			self.sock = sock
			print("Camera url: %s" % camera_url)


# This class is just for testing 
# Without async module, Real test should have at least two threads 
# One for check connection and execute command from the queue
# The other is for receiving orders and put it in the queue
class _ActiveObject:

	def __init__(self, cm):
		self.cm = cm

	def add_task(self, command):

		if not self.cm.connected:
			print("No connection ! Drop the command : %s" %command.__name__)
			return

		if self.cm.queue.full():
			print("Queue is full ! Drop the command : %s"%command.__name__)
		else:
			self.cm.queue.put(command)


if __name__ == '__main__':

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
			time.sleep(1)

			lock.acquire()
			ao.add_task(command)
			lock.release()


	thread_1 = Thread(target=target_1)
	thread_2 = Thread(target=target_2)

	print("Start the test !!! ")
	thread_1.start()
	thread_2.start()