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
		(r"/still", TakePicture)]		

    # Start the HTTP server
	def start(self):
		print("Starting Onboard HTTP Server")
		self.app = tornado.web.Application(self.routes)
		self.app.listen(8000)
		
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Main Page of Onboard Computer Web Server")
			
class TakePicture(tornado.web.RequestHandler):
	def get(self):
		self.write("Picture Page")
		asyncio.ensure_future(camera.take_picture())
		raise tornado.web.HTTPError(200)
		#yield camera.take_picture()
		#tornado.ioloop.IOLoop.current().spawn_callback(camera.take_picture())
		
		#TODO: Modify to return HTTP 400 code if call fails with reason, or HTTP 200 code if call succedes
		
class ZoomIn(tornado.web.RequestHandler):
	def get(self):
		self.write("Picture Page")
		camera.zoom_in()
		#TODO: Test for functionality

class ZoomOut(tornado.web.RequestHandler):
	def get(self):
		self.write("Picture Page")
		camera.zoom_out()
		#TODO: Test for functionality
		
