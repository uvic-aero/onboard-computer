from abc import ABC, abstractmethod
import os
import functools
import requests
import traceback
import time

__all__ = ['CameraAPI']

# TODO : Error handing for disconnection, improper command, camera dysfunction

class BaseCameraAPI(ABC):
	# Class Field
	url = ''
	liveview_url = ''
	payload = {
		"id" : 1,
		"version" : '1.0'
		}

	@classmethod
	def update_url(cls, url):
		cls.url = url

	@classmethod
	def send_command(cls, method, param = []):
		cls.payload["method"] = method
		cls.payload["params"] = param

		send_request = functools.partial(requests.post, cls.url, 
										json=cls.payload, timeout=0.5)
		
		# Make sure system doesn't crash during disconnection
		try:
			res = send_request()
		except:
			print("Some problems in connection.")
			print("Drop the command.")
			return

		# Verify status code
		if res.status_code == 200:
			res_json = res.json()  # Convert json to Python Dict
		elif res.status_code // 100 == 4:
			print("Client error - Bad request. Reset url to default.")
			print("Drop the command")
			return
		elif res.status_code // 100 == 5:
			print("Server error! Camera SSDP server problem")
			print("Drop the command")
			return
		else:
			return
		
		# Capture error message from improper command
		if "error" in res_json:
			print(res_json["error"][1])
			print("Camera is unable to execute this comand")
			print("Drop the command")
			return 
		else:
			return res_json

	@classmethod
	@abstractmethod
	def start_record_mode(cls):
		pass

	@classmethod
	@abstractmethod
	def take_still_picture(cls):
		pass
	
	@classmethod
	@abstractmethod
	def zoom_in(cls):
		pass
	
	@classmethod
	@abstractmethod
	def zoom_out(cls):
		pass
	
	@classmethod
	@abstractmethod
	def start_liveview(cls):
		pass
	
	@classmethod
	@abstractmethod
	def stop_liveview(cls):
		pass

	@classmethod
	@abstractmethod
	def check_is_IDLE(cls):
		pass


class CameraAPI(BaseCameraAPI):
	@classmethod
	def start_record_mode(cls):
		cls.send_command("startRecMode")

	@classmethod
	def still_capture(cls):
		cls._wait_until_IDLE()
		res = cls.send_command("actTakePicture")
		print("Still capture.")

		photo_url = res["result"][0][0]

		# Download image from Camera
		photo = requests.get(pic_url).content

		cur_dir = os.path.dirname(__file__)
		photo_dir = os.path.join(cur_dir, 'photo')
		photo_name = os.path.basename(photo_url)
		photo_path = os.path.join(image_dir, photo_name)

		if not os.path.exists(photo_dir):
			os.mkdir(photo_dir)

		# Save the image at .../picture folder
		with open(photo_path, 'wb') as f:
			f.write(photo)

	@classmethod
	def zoom_in(cls):
		cls._wait_until_IDLE()
		cls.send_command("actZoom", ["in", "1shot"])
		print("Zoom in.")
	
	@classmethod
	def zoom_out(cls):
		cls._wait_until_IDLE()
		cls.send_command("actZoom", ["out", "1shot"])
		print("Zoom out.")
	
	@classmethod
	def start_liveview(cls):
		cls.wait_camera_until_IDLE()
		res = cls.send_command("startLiveviewWithSize", ["L"])
		liveview_url = res['result'][0]
		cls.liveview_url = liveview_url
		print("Liveview started : %s"%liveview_url)

	@classmethod
	def stop_liveview(cls):
		cls.send_command("stopLiveview")
		cls.liveview_url = ''
		print("Liveview has been shut down.")
	
	@classmethod
	def check_is_IDLE(cls):
		status = cls._check_status()
		return (status == 'IDLE')

	@classmethod
	def _wait_until_IDLE(cls):
		while cls.check_is_IDLE() != True:
			time.sleep(0.1)

	@classmethod
	def _check_status(cls):
		res = cls.send_command("getEvent", [False])
		return res["result"][1]['cameraStatus']
