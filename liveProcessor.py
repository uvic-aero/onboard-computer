import socket
import traceback
from threading import Thread
from multiprocessing import Process, Value, Queue
from cameraAPI import RecordMode
import time
from ctypes import c_bool
from constants import framerate_delay

class LiveProcessor:
	def __init__(self, cameraManager, queue):
		self.cameraManager = cameraManager
		self.receive_queue = queue
		self.process_queue = Queue()
		self.runProcess = Value(c_bool, False)
		self.runLoop = False
		self.process = None
		self.thread = None


	def start(self):
		self.runLoop = True
		self.runProcess = True
		print("liveProcessor: Starting loops")
		print("liveProcessor: Frame delay: %f" % framerate_delay)
		try:
			self.thread = Thread(target=self.loop)
			self.process = Process(target=loop, args=(self.runProcess, self.process_queue))

			self.thread.start()
			self.process.start()
		except:
			self.process = None
			self.thread = None
			print("liveProcessor: Failed to start thread")

	def stop(self):
		self.runLoop = False
		self.runProcess = False

		if self.process:
			self.process.join()

	def loop(self):
		print("liveProcessor: Entering receive loop")
		while self.runLoop == True:
			if self.cameraManager.connected == False:
				print("liveProcessor: Camera not connected")
				time.sleep(1)
				continue

			if self.cameraManager.currentMode != RecordMode.LIVE:
				time.sleep(1)
				continue

			time.sleep(framerate_delay)

			if self.receive_queue.empty():
				continue
			
			image = self.receive_queue.get()

			if self.process_queue.qsize() == 0:
				self.process_queue.put(image)

def loop(runLoop, queue):
	connections = []
	server = None
	server_started = False
	
	print("liveProcessor: Entering process loop")
	while runLoop == True:

		if server_started == False:
			server_started, server = start_server(server_started, server)

		check_connections(server, server_started, connections)

		time.sleep(framerate_delay)

		if queue.empty():
			continue

		image = queue.get()

		broadcast_image(connections, image)

	print("liveProcessor: Stopping process loop")
	if server:
		stop_server(server)

def start_server(server_started, server):
	if server_started == False:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind(('0.0.0.0', 5000))
		server.listen(2)
		server.setblocking(0)

		print("liveProcessor: Server listening")
		server_started = True
	return server_started, server

def check_connections(server, server_started, connections):
	if server == None or server_started == False:
		return

	try:
		conn, addr = server.accept()

		message = "\r\n".join([
			'HTTP/1.1 200 OK',
			'Content-Type: multipart/x-mixed-replace;boundary=frame',
			'', ''])

		conn.send(message.encode())

		connections.append(conn)
		print("liveProcessor: New listener")
	except:
		# An exception means no incoming connection
		return

def broadcast_image(connections, image):

	for conn in connections[:]:
		try:
			conn.send( b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n' % len(image))
			conn.send(image)
			conn.send(b'\r\n')
		except socket.timeout:
			pass
		except (BrokenPipeError, OSError):
			connections.remove(conn)
			print("The connection has been shut down or closed.")
		except AttributeError:
			pass
		except:
			connections.remove(conn)

def stop_server(server):

	server.close()
	server = None
	#self.server_started = False


