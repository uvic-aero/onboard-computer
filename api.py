import tornado.ioloop
import tornado.web
import asyncio
import json

# An HTTP server that will receive commands from the GroundStation
class API:

	def __init__(self, cameraManager):
		self.cameraManager = cameraManager

		params = dict(cameraManager=cameraManager)

		self.routes = [
			(r"/", MainHandler),
			(r"/zoom/in", ZoomIn, params),
			(r"/zoom/out", ZoomOut, params),
			(r"/still", TakePicture, params),
			(r"/mode", CameraMode, params),
			(r"/status", CameraStatus, params)]
		
    # Start the HTTP server
	def start(self):
		self.app = tornado.web.Application(self.routes)
		self.app.listen(8000)
		print("Onboard HTTP Server Running")	

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Main Page of Onboard Computer Web Server")
			
class TakePicture(tornado.web.RequestHandler):
	def initialize(self, cameraManager):
		self.cameraManager = cameraManager
	def get(self):
		self.cameraManager.api.still_capture()
		
class ZoomIn(tornado.web.RequestHandler):
	def initialize(self, cameraManager):
		self.cameraManager = cameraManager
	def get(self):
		self.cameraManager.api.zoom_in()

class ZoomOut(tornado.web.RequestHandler):
	def initialize(self, cameraManager):
		self.cameraManager = cameraManager
	def get(self):
		self.cameraManager.api.zoom_out()

class CameraMode(tornado.web.RequestHandler):
	def initialize(self, cameraManager):
		self.cameraManager = cameraManager
	def get(self):
		cmode = self.cameraManager.currentMode
		wmode = self.cameraManager.wantedMode
		self.write({'current': int(cmode), 'wanted': int(wmode)})

	def post(self):
		print(self.request.body)
		_json = json.loads(self.request.body, encoding = object)
		print(_json)
		if 'wanted' in _json:
			mode = _json['wanted']

			if mode == 1 or mode == 2:
				self.cameraManager.wantedMode = mode
			else:
				self.set_status(403)
		else:
			self.set_status(403)

class CameraStatus(tornado.web.RequestHandler):
	def initialize(self, cameraManager):
		self.cameraManager = cameraManager

	@tornado.web.asynchronous
	def get(self):
		self.cameraManager.api.check_status(self._get_status_result)

	def _get_status_result(self, res):
		if res is None:
			self.write({'status': 'unknown'})
		else:
			self.write({'status': res["result"][1]['cameraStatus'] })

		self.finish()

		

		
