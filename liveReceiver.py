from liveProcessor import LiveProcessor
import threading
from cameraAPI import RecordMode
import time
import socket
from urllib.parse import urlparse
import binascii
from queue import Queue

class LiveReceiver:

	def __init__(self, cameraManager):
		self.cameraManager = cameraManager
		self.queue = Queue()
		self.runLoop = False
		self.processor = LiveProcessor(cameraManager, self.queue)
		self.liveview_started = False
		self.liveview_running = False
		self.liveview_connected = False
		self.liveview_url = ''
		self.client = None

	def start(self):
		self.runLoop = True;
		try:
			t = threading.Thread(target=self.loop)
			t.start()
		except:
			print ("Error starting liveReceiver and/or liveProcessor Threads")

		self.processor.start()
		
	def stop(self):
		print("liveReceiver: Stopping")
		self.processor.stop()
		self.runLoop = False
		self.cameraManager.api.stop_liveview(self._stop_liveview_result)

	def _start_liveview(self):
		print("liveReceiver: Starting liveview")
		self.liveview_started = True
		self.cameraManager.api.start_liveview(self._start_liveview_result)

	def _stop_liveview_result(self, res):
		if res is not None:
			self.liveview_url = ''
			print("Liveview has been shut down.")

	def _start_liveview_result(self, res):

		if res is None:
			return None

		liveview_url = res['result'][0]
		self.liveview_url = liveview_url
		print("Liveview started : %s"%liveview_url)
		self.cameraManager.currentMode = RecordMode.LIVE

	def _create_connection(self):

		print("liveReceiver: Creating connection")

		self.hostname = urlparse(self.liveview_url).hostname
		self.port = urlparse(self.liveview_url).port
		self.path = urlparse(self.liveview_url).path

		self.client = socket.create_connection((self.hostname, self.port))
		print("liveReceiver: Sucessfully connect to camera liveview stream")

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

		print("liveReceiver: Received camera connection reponse")
		self.liveview_connected = True

	def loop(self):
		print("liveReceiver: Loop running")
		frames = 0
		while self.runLoop == True:
			if self.cameraManager.connected == False:
				print("liveReceiver: Camera not connected")
				time.sleep(5)
				continue

			if self.cameraManager.wantedMode != RecordMode.LIVE:
				print("liveReceiver: Liveview mode not wanted")
				time.sleep(3)
				continue

			if self.cameraManager.currentMode != RecordMode.LIVE:
				print("liveReceiver: Putting camera into liveview mode")
				if self.liveview_started == False:
					self._start_liveview()
				print("liveReceiver: Waiting for liveview to start")
				time.sleep(2)
				continue

			if self.liveview_running == False:
				if self.liveview_connected == False:
					self._create_connection()
					time.sleep(2)
					continue

				self.liveview_running = True
	
			raw_image = self._receive_image()

			if raw_image:
				print("liveReceiver: Queued next image")
				self.queue.put(raw_image)
			else:
				continue

			print("liveReceiver: Frame %s" % frames)
			frames += 1


	def _receive_image(self):

		try:
			data = self.client.recv(1, socket.MSG_WAITALL)

			print(len(data))

			if len(data) == 0:
				return None

			start_byte = data[0]

			# 255 dictates start of new header+payload
			if start_byte != 255:
				return None

			# Read rest of info header
			data = self.client.recv(7, socket.MSG_WAITALL)

			print(len(data))

			# Sanity check the payload type
			payload_type = data[0] # 1 or 2

			if payload_type != 1:
				skipped_bytes += 1
				return None

			sequence_number = int(binascii.hexlify(data[1:3]), 16)
			time_stamp = int(binascii.hexlify(data[3:7]), 16)

			# Read payload header
			data = self.client.recv(128, socket.MSG_WAITALL)

			print(len(data))

			start_code = int(binascii.hexlify(data[0:4]), 16)
			jpeg_data_size = int(binascii.hexlify(data[4:7]), 16)
			padding_size = data[7]

			_image_width = int(binascii.hexlify(data[7:9]), 16)
			_image_height = int(binascii.hexlify(data[9:11]), 16)

			# Read actual payload
			chunks = []
			received = 0
			while received < jpeg_data_size:
				chunk = self.client.recv(min(jpeg_data_size - received, 2048), socket.MSG_WAITALL)

				if chunk == b'':
					return None

				received += len(chunk)
				chunks.append(chunk)

			print(received, jpeg_data_size)

			if padding_size > 0:
				self.client.recv(padding_size, socket.MSG_WAITALL)

			return b''.join(chunks)

		except Exception as e:
			print(str(e))
			return None