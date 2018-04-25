import os
import functools
import requests
import traceback
import time
import enum
from queue import Queue

__all__ = ['CameraAPI']

class RecordMode(enum.Enum):
	NONE = 0
	STILL = 1
	LIVE = 2

# TODO : Error handing for disconnection, improper command, camera dysfunction

class BaseCameraAPI():

	def __init__(self, manager):
		self.manager = manager
		self.url = ''
		self.liveview_url = ''
		self.payload = {
			"id" : 1,
			"version" : '1.0'
		}
		self.queue = Queue()

	def _process_queue(self):
		if not self.queue.empty():
			method, callback, params = self.queue.get()

			self._send_command(method, callback, params)

	def _update_url(self, url):
		self.url = url

	def _queue_command(self, method, callback = None, params = []):
		print("Queued command %s" % method)
		self.queue.put( (method, callback, params) )
		
	def _send_command(self, method, callback, params):
		print("Sending command %s" % method)
		self.payload["method"] = method
		self.payload["params"] = params

		# Make sure system doesn't crash during disconnection
		# Timeout must be set >= 3.5s,  because camera responds very slow
		# Probably need to add api for setting timeout from ground station
		# considered the possibility of different time to download different
		# images
		try:
			res = requests.post(self.url, json=self.payload, 
				timeout=3.5)
		except:
			print("Drop the command : %s - No connection."%method)
			return

		# Verify status code
		if res.status_code == 200:
			res_json = res.json()  # Convert json to Python Dict
		elif res.status_code // 100 == 4:
			print("Drop the command : %s - Client error, Bad request."%method)
			return
		elif res.status_code // 100 == 5:
			print("Drop the command : %s - "%method, 
				"Server error! Camera SSDP server problem.")
			return
		else:
			print("Drop the command : %s - Something wrong."%method)
			return
		
		# Capture error message from improper command
		if "error" in res_json:
			print(res_json["error"][1])
			print("Drop the command : %s - "%method, 
				"Camera NotReady ! Please start record mode.")
			return 
		else:
			if callback is not None:
				callback(res_json)

	def start_record_mode(self):
		pass

	def still_capture(self):
		pass

	def zoom_in(self):
		pass

	def zoom_out(self):
		pass

	def start_liveview(self):
		pass

	def stop_liveview(self):
		pass

	def check_is_IDLE(self):
		pass


class CameraAPI(BaseCameraAPI):

	def __init__(self, manager):
		super().__init__(manager)

	def start_record_mode(self):
		self._queue_command("startRecMode", self._start_record_mode_result)

	def _start_record_mode_result(self, res):
		if res is None:
			return 

		if 'result' in res:
			self.manager.currentMode = RecordMode.STILL

	def still_capture(self, callback):
		self._queue_command("actTakePicture", callback if callback is not None else self._still_capture_result)

	def _still_capture_result(self, res):

		if res is None:
			return 
		
		photo_url = res["result"][0][0]

		print("Still capture.")

		# Download image from Camera
		photo = requests.get(photo_url).content

		cur_dir = os.path.dirname(__file__)
		photo_dir = os.path.join(cur_dir, 'images')
		photo_name = os.path.basename(photo_url)
		photo_path = os.path.join(photo_dir, photo_name)

		if not os.path.exists(photo_dir):
			os.mkdir(photo_dir)

		# Save the image at .../picture folder
		with open(photo_path, 'wb') as f:
			f.write(photo)

	def zoom_in(self):
		self._queue_command("actZoom", params=["in", "1shot"])
		print("Zoom in.")
	
	def zoom_out(self):
		self._queue_command("actZoom", params=["out", "1shot"])
		print("Zoom out.")

	def start_liveview(self, callback):
		self._queue_command("startLiveview", callback)

	def stop_liveview(self, callback):
		self._queue_command("stopLiveview", callback)
	
	
	def check_is_IDLE(self):
		return None
		'''
		status = self._check_status()

		if status is None:
			return None

		return (status == 'IDLE')
		'''

	def check_status(self):
		self._queue_command("getEvent", self._check_status_result, params=[False])

	def _check_status_result(self, res):
		if res is None:
			return

		return res["result"][1]['cameraStatus']
