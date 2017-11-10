import tornado.ioloop
import tornado.web
import asyncio
from camera import camera

# An HTTP server that will receive commands from the GroundStation
class API:

	def __init__(self):
		self.routes = [(r"/", MainHandler),
		(r"/zoom/in", ZoomIn),
		(r"/zoom/out", ZoomOut),
		(r"/status", Status),
		(r"/still", TakePicture)]		
		
		
    # Start the HTTP server
	def start(self):
		self.app = tornado.web.Application(self.routes)
		self.app.listen(8000)
		print("Onboard HTTP Server Running")

	
		
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Main Page of Onboard Computer Web Server")
			
class TakePicture(tornado.web.RequestHandler):
	def get(self):
		if(camera.connected):
			self.write("Picture Page")
			asyncio.ensure_future(camera.take_picture())
			raise tornado.web.HTTPError(200)
		else:
			raise tornado.web.HTTPError(503)

		
class ZoomIn(tornado.web.RequestHandler):
	def get(self):
		if(camera.connected):
			self.write("Zoom In Page")
			camera.zoom_in()
			raise tornado.web.HTTPError(200)
		else:
			raise tornado.web.HTTPError(503)
		
		#TODO: Test for functionality

class ZoomOut(tornado.web.RequestHandler):
	def get(self):
		if(camera.connected):
			self.write("Zoom Out Page")
			camera.zoom_out()
			raise tornado.web.HTTPError(200)
		else:
			raise tornado.web.HTTPError(503)
		#TODO: Test for functionality

class Status(tornado.web.RequestHandler):
	def get(self):
		self.write("Status: " + camera.status.name)
		if camera.status.value == 0:
			self.set_status(200,reason=None)
		if camera.status.value == 1:
			self.set_status(503,reason=None)
		if camera.status.value > 1:
			self.set_status(500,reason=None)
		else:
			self.set_status(500,reason=None)

		

		
