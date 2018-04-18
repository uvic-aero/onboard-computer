import time
import threading

class StillProcessor:
	def __init__(self, cameraManager, queue):
		self.cameraManager = cameraManager
		self.queue = queue
		self.runLoop = False

	def loop(self):
		print("stillProcessor: Entering loop")
		while(self.runLoop):
			if self.queue.empty():
				print("stillProcessor: Queue is empty")
				time.sleep(3)
				continue

			item = self.queue.get()

			print("stillProcessor: Received item for processing")

	def start(self):
		print("Starting Still Processor")
		self.runLoop = True
		try:
			t = threading.Thread(target=self.loop)
			t.start()
		except:
			print ("Error starting stillProcessor thread")
		
	def stop(self):
		print("Stopping still processor")
		self.runLoop = False;