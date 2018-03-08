
from abc import ABC, abstractmethod
import os
import functools
import requests
import traceback
import time

__all__ = ['cameraAPI']

# TODO : Add Camera Exception

class BaseCameraAPI(ABC):
	def __init__(self):
		self.url = ''
		self.payload = {
			"id" : 1,
			"version" : '1.0',
		}
		self.liveview_url = ''

	def send_command(self, method, param = []):
		self.payload["method"] = method
		self.payload["params"] = param

		send_request = functools.partial(requests.post, self.url, json=self.payload)
		
		# Send request to the camera and make sure it does response
		try:
			res = send_request()
			res.status_code
		except Exception as e:
			traceback.print_exc()
			raise Exception("The camera didn't respond or the camera url didn't work.")

		# Verify status code
		if res.status_code == 200:
			res_json = res.json()  # Convert json to Python Dict
		else:
			raise Exception("Response status code: %s" % res.status_code)
		
		# Capture error message from camera, otherwise return res_json
		if "error" in res_json:
			raise Exception(res_json["error"][1])
		else:
			return res_json
	
	def update_url(self, url):
		self.url = url

	@abstractmethod
	def take_still_picture(self):
		pass
	
	@abstractmethod
	def zoom_in(self):
		pass
	
	@abstractmethod
	def zoom_out(self):
		pass
	
	@abstractmethod
	def start_liveview(self):
		pass
	
	@abstractmethod
	def stop_liveview(self):
		pass

	@abstractmethod
	def check_is_IDLE(self):
		pass


class CameraAPI(BaseCameraAPI):
	def take_still_picture(self):
		self._wait_until_IDLE()
		res = self.send_command("actTakePicture")
		pic_url = res["result"][0][0]

		# Download image from Camera
		image = requests.get(pic_url).content

		cur_dir = os.path.dirname(__file__)
		image_dir = os.path.join(cur_dir, 'picture')
		pic_name = os.path.basename(pic_url)
		pic_path = os.path.join(image_dir, pic_name)

		if not os.path.exists(image_dir):
			os.mkdir(image_dir)

		# Save the image at .../picture folder
		with open(pic_path, 'wb') as f:
			f.write(image)

	def zoom_in(self):
		self._wait_until_IDLE()
		self.send_command("actZoom", ["in", "1shot"])
	
	def zoom_out(self):
		self._wait_until_IDLE()
		self.send_command("actZoom", ["out", "1shot"])
	
	def start_liveview(self):
        self.wait_camera_until_IDLE()
        res = self.send_command("startLiveviewWithSize", ["L"])
        liveview_url = res['result'][0]
        self.liveview_url = liveview_url
        print("Liveview url : %s"%liveview_url)

	def stop_liveview(self):
		self.send_command("stopLiveview")
		self.liveview_url = ''
		print("Liveview has been shut down.")
	
	def check_is_IDLE(self):
		status = self._check_status()
		return (status == 'IDLE')

	def _wait_until_IDLE(self):
		while self.check_is_IDLE() == False:
			time.sleep(0.05)

	def _check_status(self):
        res = self.send_command("getEvent", [False])
        return res["result"][1]['cameraStatus']


cameraAPI = CameraAPI()
