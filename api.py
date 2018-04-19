import tornado.ioloop
import tornado.web
import asyncio

# An HTTP server that will receive commands from the GroundStation
class API:

	def __init__(self, cameraManager):
		self.cameraManager = cameraManager

		params = dict(cameraManager=cameraManager)

		self.routes = [
			(r"/", MainHandler),
			(r"/zoom/in", ZoomIn, params),
			(r"/zoom/out", ZoomOut, params),
			(r"/status", Status, params),
			(r"/still", TakePicture, params)]
		
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
		pass
		
class ZoomIn(tornado.web.RequestHandler):
	def initialize(self, cameraManager):
		self.cameraManager = cameraManager
	def get(self):
		pass

class ZoomOut(tornado.web.RequestHandler):
	def initialize(self, cameraManager):
		self.cameraManager = cameraManager
	def get(self):
		pass
		
class Status(tornado.web.RequestHandler):
	def initialize(self, cameraManager):
		self.cameraManager = cameraManager
	def get(self):
		pass

		

		
