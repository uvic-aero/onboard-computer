from liveProcessor import LiveProcessor
import threading
from queue import Queue

class LiveReceiver:

	def __init__(self, CameraManager):
		self.image_queue = Queue();
		self.runLoop = False;

	def loop(self):
		print("Loop Running")
		print(self.runLoop)
		while(self.runLoop):
			self.handle_receiver()
			
	def start(self):
		self.runLoop = True;
		try:
			t = threading.Thread(target=self.loop)
			t.start()
		except:
			print ("Error starting liveReceiver and/or liveProcessor Threads")
		
	def stop(self):
		self.runLoop = False;
		
	def handle_receiver(self):
		print("Loop Foreverrrrrrrrrrr")
	