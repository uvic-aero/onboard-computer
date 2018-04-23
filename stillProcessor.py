import time
import threading
import requests
import base64

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

			image = self.queue.get()

			print("stillProcessor: Received item for processing")

			self.send_image(image)

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

	def send_image(self, image):
	
		try:
			print(type(image))
			timestamp = time.time() * 1000
			#encoded_image = base64.b64encode(image)
			encoded_image = base64.b64encode(image)

			print(type(encoded_image))

			payload = {
				'timestamp': timestamp,
				'image': encoded_image.decode('utf-8', "ignore")
			}

			requests.post('http://localhost:24002/images', json=payload)

		except Exception as e:
			print(str(e))
			print("Failed to send image to groundstation")