from stillProcessor import StillProcessor
from cameraAPI import RecordMode
import threading
import time
from queue import Queue

class StillReceiver:
	def __init__(self, cameraManager):
		self.cameraManager = cameraManager
		self.image_queue = Queue();
		self.runLoop = False
		self.processor = StillProcessor(cameraManager, self.image_queue)
		self.capturing = False

	def loop(self):
		print("stillReceivver: Entering loop")
		while(self.runLoop):
			self.handle_receiver()
			
	def start(self):
		self.runLoop = True;
		try:
			t = threading.Thread(target=self.loop)
			t.start()
		except:
			print ("Error starting stillReceiver")

		self.processor.start()
		
	def stop(self):
		print("Stopping still receiver")
		self.runLoop = False
		self.processor.stop()
		
	def handle_receiver(self):
		if self.cameraManager.connected == False:
			print("stillReceiver: Camera not connected")
			time.sleep(5)
			return

		if self.cameraManager.recMode != RecordMode.STILL:
			print("stillReceiver: Camera not in Still mode")
			self.cameraManager.api.start_record_mode()
			time.sleep(5)
			return

		if self.capturing == True:
			print("Waiting on image capture")
			time.sleep(1)
			return

		print("Capturing picture")
		self.cameraManager.api.still_capture(self.handle_image)
		self.capturing = True

	def handle_image(self, result):
		print("Captured image")
		self.capturing = False


