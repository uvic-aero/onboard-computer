from liveProcessor import LiveProcessor

class LiveReceiver:
	def __init__(CameraManager):
		self.live_queue = Queue();
		self.runLoop = false;
	def loop():
		while(runLoop):
			handle_receiver()
			
	def start():
		runLoop = true;
		thread.start_new_thread(loop, ())
		
	def stop():
		runLoop = false;
		
	def handle_receiver():
	