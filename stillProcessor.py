import time
import threading
import requests
import base64
import os
from constants import groundstation_url

class StillProcessor:
	def __init__(self, cameraManager, queue):
		self.cameraManager = cameraManager
		self.queue = queue
		self.runLoop = False

	def loop(self):
		print("stillProcessor: Entering loop")
		while(self.runLoop):
			if self.queue.empty():
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

	def _save_image(self, image):
		cur_dir = os.path.dirname(__file__)
		photo_dir = os.path.join(cur_dir, 'images')
		photo_name = os.path.basename(str(time.time()) + '.jpg')
		photo_path = os.path.join(photo_dir, photo_name)

		if not os.path.exists(photo_dir):
			os.mkdir(photo_dir)

		# Save the image at .../picture folder
		with open(photo_path, 'wb') as f:
			f.write(image)

	def send_image(self, image):
	
		self._save_image(image)

		try:
			timestamp = time.time() * 1000
			#encoded_image = base64.b64encode(image)
			encoded_image = base64.b64encode(image)

			payload = {
				'timestamp': timestamp,
				'image': encoded_image.decode('utf-8', "ignore")
			}

			requests.post(groundstation_url + '/images', json=payload)

		except Exception as e:
			print(str(e))
			print("Failed to send image to groundstation")