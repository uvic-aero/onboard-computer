from cameraAPI import CameraAPI
from http.client import HTTPResponse
from io import BytesIO

import xml.etree.ElementTree as ET
import netifaces
import requests
import socket
import time


__all__ = ['ClassManager']

# TODO : Decide how to monitor connection and execute commands concurrently

class FakeSocket:
	def __init__(self, response_str):
		self._file = BytesIO(response_str)
	def makefile(self, *args, **kwargs):
		return self._file

class ConnHandler:
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

	@classmethod
	def get_sock_location(cls, sock):
		message = cls.ssdp_req
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
	# Class Field
	api = CameraAPI
	handler = ConnHandler
	connected = False
	sock = socket.socket()

	# TODO
	@classmethod
	def start(cls):
		while True:
			cls.connected = cls._check_connection()
			if cls.connected:
				print("Sock works")
				time.sleep(0.5)
			else:
				print("Try to reconnect!")
				addresses = cls.handler.scan_netifaces()
				for addr in addresses:
					if cls._connect(addr):
						break
				time.sleep(0.5)

	@classmethod
	def _check_connection(cls):
		url = cls.api.url
		payload = cls.api.payload
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
			return True

	@classmethod
	def _connect(cls, addr):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		sock.settimeout(0.5)

		sock.bind((addr, 0))

		location = cls.handler.get_sock_location(sock)
		if location is None:
			sock.close()
		else:
			camera_url = cls.handler.get_camera_url(location)
			cls.api.update_url(camera_url)
			cls.connected = True
			cls.sock.close()
			cls.sock = sock
			print("Camera url: %s" % camera_url)

if __name__ == '__main__':
	CameraManager.start()
