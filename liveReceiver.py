from liveProcessor import LiveProcessor
import threading


class LiveReceiver:

	def __init__(self, cameraManager):
		self.cameraManager = cameraManager
		self.runLoop = False
		self.processor = LiveProcessor(cameraManager)

	def loop(self):
		print("Loop Running : ", self.runLoop)
		while(self.runLoop):
			self.handle_receiver()
			
	def start(self):
		self.runLoop = True;
		try:
			t = threading.Thread(target=self.loop)
			t.start()
		except:
			print ("Error starting liveReceiver and/or liveProcessor Threads")

		self.processor.start()
		
	def stop(self):
		self.processor.stop()
		self.runLoop = False
		self.cameraManager.api.stop_liveview()
		
	def handle_receiver(self):
		liview_url = self.cameraManager.api.liveview_url
		if not liveview_url:
			self.cameraManager.api.start_liveview()
