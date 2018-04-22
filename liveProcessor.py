import socket
import binascii
import traceback
from threading import Thread
from urllib.parse import urlparse


class LiveProcessor:
	def __init__(self, cameraManager):
		self.cameraManager = cameraManager
		self.conn = None
		self.server = None
		self.client = None
		self.hostname = None
		self.port = None
		self.path = None

	def start(self):
		liveview_url = self.cameraManager.api.liveview_url
		self.hostname = urlparse(liveview_url).hostname
		self.port = urlparse(liveview_url).port
		self.path = urlparse(liveview_url).path

		t_server = Thread(target=_start_server)
		t_client = Thread(target=_start_client)

		t_server.start()
		t_client.start()

	def stop(self):
		self._stop_client()
		self._stop_server()

		self.hostname = None
		self.port = None
		self.path = None

	def _start_server(self):
		if self.server is None:
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server.bind(('127.0.0.1', 5000))
			server.listen(2)

			try:
				conn, addr = server.accept()
			except ConnectionAbortedError as ex:
				return
			else:
				self.conn = conn
				self.server = server
				print("Started liveview server on 127.0.0.1:5000")

	def _start_client(self):
		client = socket.create_connection((self.hostname, self.port))
		print("Sucessfully connect to camera liveview stream")

		self.client = client

		self._prime()

		frames = 1

		while self.client:

			raw_image = self._preprocess()

			if raw_image:
				self._broadcast_image(raw_image)
			else:
				continue

			print("Frame: %s" % frames)
			frames += 1

	def _prime(self):

		# Send raw HTTP request to initiate data flow
		request = "\r\n".join([
			'GET %s HTTP/1.1' % self.path,
			'HOST: %s:%s' % (self.hostname, self.port),
			'ACCEPT: */*',
			'', ''])

		try:
			self.client.send(request.encode())
		except (BrokenPipeError, OSError) as ex:
			return None
		except AttributeError:
			return None

		# Read initial HTTP response
		# b'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nTransfer-Encoding: chunked\r\n\r\n6788\r\n'
		self.client.recv(95)

	def _preprocess(self):

		try:
			data = self.client.recv(1, socket.MSG_WAITALL)
		except OSError:
			# return None when socket is closed
			return None
		except AttributeError:
			# in case that self.client is set to 'None'
			return None
		else:
			if len(data) == 0:
				# return None when socket is shutdown
				return None

			start_byte = data[0]

			# 255 dictates start of new header+payload
			if start_byte != 255:
				return None

		# Read rest of info header
		try:
			data = self.client.recv(7, socket.MSG_WAITALL)
		except OSError:
			return None
		except AttributeError:
			return None
		else:
			if len(data) == 0:
				# return None when socket is shutdown
				return None

			# Sanity check the payload type
			payload_type = data[0] # 1 or 2

			if payload_type != 1:
				return None

			sequence_number = int(binascii.hexlify(data[1:3]), 16)
			time_stamp = int(binascii.hexlify(data[3:7]), 16)

		# Read payload header
		try:
			data = self.client.recv(128, socket.MSG_WAITALL)
		except OSError:
			return None
		except AttributeError:
			return None
		else:
			start_code = int(binascii.hexlify(data[0:4]), 16)
			jpeg_data_size = int(binascii.hexlify(data[4:7]), 16)
			padding_size = data[7]

			_image_width = int(binascii.hexlify(data[7:9]), 16)
			_image_height = int(binascii.hexlify(data[9:11]), 16)

		# Read actual payload
		try:
			raw_image = self.client.recv(jpeg_data_size, socket.MSG_WAITALL)
		except OSError:
			return None
		except AttributeError:
			return None

		# Retrieve and omit padding
		if padding_size > 0:
			try:
				self.client.recv(padding_size, socket.MSG_WAITALL)
			except OSError:
				pass
			except AttributeError:
				pass

		return raw_image

	def _broadcast_image(self, image):
		
		message = b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %d' % len(image) + b'\r\n\r\n' + image + b'\r\n'

		if self.conn:
			try:
				self.conn.send(message)
			except (BrokenPipeError, OSError) as ex:
				print("The connection has been shut down or closed.")
			except AttributeError:
				pass
			except:
				traceback.print_exc()

	def _stop_client(self):

		self.conn.shutdown(socket.SHUT_RDWR)
		self.conn.close()
		self.conn = None

		self.client.shutdown(socket.SHUT_RDWR)
		self.client.close()
		self.client = None

	def _stop_server(self):

		self.server.close()
		self.server = None
