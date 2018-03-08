from stillProcessor import StillProcessor
import thread

class StillReceiver:
	def __init__(CameraManager):
		self.image_queue = Queue();
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
	

	
	