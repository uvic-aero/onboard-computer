import tornado.ioloop
import tornado.web
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
		self.app = tornado.web.Application(self.routes)
		self.app.listen(8000)
		tornado.ioloop.IOLoop.current().start()
		
	def stop(self):
		tornado.ioloop.IOLoop.current().stop()
		
		
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Main Page of Onboard Computer Web Server	")
			
class TakePicture(tornado.web.RequestHandler):
	def get(self):
		self.write("Picture Page")
		camera.take_picture()
		#TODO: Listed Below
		#Return an HTTP 200 if the call succeeded 
		#400-level code if the call failed with reason
		#This call will depend on the camera being in Liveview mode to tell the camera to capture a still image
		#will pause the liveview until the image is complete. This call may take many seconds to complete,
		#but should not block the rest of the API***
		

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
		

#For Debugging Use (Running Independantly for now):
if __name__ == "__main__":
	server = API()
	server.start()