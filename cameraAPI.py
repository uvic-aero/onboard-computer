import os
import functools
import requests
import traceback
import time

__all__ = ['CameraAPI']

# TODO : Error handing for disconnection, improper command, camera dysfunction

class BaseCameraAPI():

	def __init__(self):
		self.url = ''
		self.liveview_url = ''
		self.payload = {
			"id" : 1,
			"version" : '1.0'
		}

	def update_url(self, url):
		self.url = url

	def send_command(self, method, param = []):
		self.payload["method"] = method
		self.payload["params"] = param

		# Make sure system doesn't crash during disconnection
		# Timeout must be set >= 3.5s,  because camera responds very slow
		# Probably need to add api for setting timeout from ground station
		# considered the possibility of different time to download different
		# images
		try:
			res = requests.post(self.url, json=self.payload, 
				timeout=3.5)
		except:
			print("Some problems in connection.")
			print("Drop the command : %s"%method)
			return

		# Verify status code
		if res.status_code == 200:
			res_json = res.json()  # Convert json to Python Dict
		elif res.status_code // 100 == 4:
			print("Client error - Bad request. Reset url to default.")
			print("Drop the command : %s"%method)
			return
		elif res.status_code // 100 == 5:
			print("Server error! Camera SSDP server problem")
			print("Drop the command : %s"%method)
			return
		else:
			return
		
		# Capture error message from improper command
		if "error" in res_json:
			print(res_json["error"][1])
			print("NotReady ! Please start record mode")
			print("Drop the command : %s"%method)
			return 
		else:
			return res_json

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

	def start_record_mode(self):
		self.send_command("startRecMode")

	def still_capture(self):
		res = self.send_command("actTakePicture")

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
		print("Photo dir : ", photo_dir)
		print("Photo path : ", photo_path)

		if not os.path.exists(photo_dir):
			os.mkdir(photo_dir)

		# Save the image at .../picture folder
		with open(photo_path, 'wb') as f:
			f.write(photo)

	def zoom_in(self):
		self.send_command("actZoom", ["in", "1shot"])
		print("Zoom in.")
	
	def zoom_out(self):
		self.send_command("actZoom", ["out", "1shot"])
		print("Zoom out.")

	def start_liveview(self):
		res = self.send_command("startLiveviewWithSize", ["L"])

		if res is None:
			return None

		liveview_url = res['result'][0]
		self.liveview_url = liveview_url
		print("Liveview started : %s"%liveview_url)

	def stop_liveview(self):
		res = self.send_command("stopLiveview")
		if res is not None:
			self.liveview_url = ''
			print("Liveview has been shut down.")
	
	def check_is_IDLE(self):
		status = self._check_status()

		if status is None:
			return None

		return (status == 'IDLE')


	def _check_status(self):
		res = self.send_command("getEvent", [False])

		if res is None:
			return

		print (res["result"][1]['cameraStatus'])
		return res["result"][1]['cameraStatus']
