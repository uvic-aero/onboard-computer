import socket
import traceback
from threading import Thread
from cameraAPI import RecordMode
import time

class LiveProcessor:
	def __init__(self, cameraManager, queue):
		self.cameraManager = cameraManager
		self.queue = queue
		self.runLoop = False
		self.connections = []
		self.server = None
		self.server_started = False

	def start(self):
		self.runLoop = True
		try:
			t_server = Thread(target=self.loop)

			t_server.start()
		except:
			print("liveProcessor: Failed to start thread")

	def stop(self):
		self.runLoop = False

		if self.server_started:
			self._stop_server()

	def loop(self):
		print("liveProcessor: Entering loop")
		while self.runLoop == True:
			if self.cameraManager.connected == False:
				print("liveProcessor: Camera not connected")
				time.sleep(5)
				continue

			if self.cameraManager.currentMode != RecordMode.LIVE:
				time.sleep(3)
				continue 

			if self.server_started == False:
				self._start_server()

			self._check_connections()

			if self.queue.empty():
				continue

			image = self.queue.get()

			self._broadcast_image(image)

	def _start_server(self):
		if self.server_started == False:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.bind(('127.0.0.1', 5000))
			self.server.listen(2)
			self.server.setblocking(0)

			print("liveProcessor: Server listening")
			self.server_started = True

	def _check_connections(self):
		if self.server == None or self.server_started == False:
			return

		try:
			conn, addr = self.server.accept()

			message = "\r\n".join([
				'HTTP/1.1 200 OK',
				'Content-Type: multipart/x-mixed-replace;boundary=frame',
				'', ''])

			conn.send(message.encode())

			self.connections.append(conn)
			print("liveProcessor: New listener")
		except:
			# An exception means no incoming connection
			return

	def _broadcast_image(self, image):

		with open('image.jpg', 'wb') as f:
			f.write(image)

		print(len(image))
		
		message = b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %d' % len(image) + b'\r\n\r\n' + image + b'\r\n'

		print("liveProcessor: Broadcasting image")

		for conn in self.connections[:]:
			try:
				
				conn.send(message)
			except (BrokenPipeError, OSError) as ex:
				self.connections.remove(conn)
				print("The connection has been shut down or closed.")
			except AttributeError:
				pass
			except:
				self.connections.remove(conn)

	def _stop_server(self):

		self.server.close()
		self.server = None
		self.server_started = False
