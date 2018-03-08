from stillProcessor import StillProcessor
import threading
from queue import Queue

class StillReceiver:
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
			print ("Error starting stillReceiver and/or stillProcessor Threads")
		
	def stop(self):
		runLoop = False;
		
	def handle_receiver(self):
		print("Loop Foreverrrrrrrrrrr")

