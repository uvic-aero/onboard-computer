import tornado.ioloop
import tornado.web
from camera import camera
# An HTTP server that will receive commands from the GroundStation
class API:
    
	def __init__(self):
		self.routes = [(r"/", MainHandler),
		(r"/zoom/in", ZoomIn),
		(r"/zoom/out", ZoomOut),
		(r"/STILL", TakePicture)]
		

    # Start the HTTP server
	def start(self):
		self.app = tornado.web.Application(self.routes)
		self.app.listen(8000)
		tornado.ioloop.IOLoop.current().start()
		
	def stop(self):
		tornado.ioloop.IOLoop.current().stop()
		
		
class MainHandler(tornado.web.RequestHandler): #All Functions in Class Camera
	def get(self):
		self.write("Main Page of Onboard Computer Web Server	")
			
class TakePicture(tornado.web.RequestHandler):
	def get(self):
		self.write("Picture Page")
		#TODO: Call Capture function on Camera
		#take_picture(self)

class ZoomIn(tornado.web.RequestHandler):
	def get(self):
		self.write("Picture Page")
		#TODO: Call Zoom In function on Camera
		#zoom_in(self)

class ZoomOut(tornado.web.RequestHandler):
	def get(self):
		self.write("Picture Page")
		#TODO: Call Zoom out function on Camera
		#zoom_out(self)		
		

#For Debugging Use (Running Independantly for now):
if __name__ == "__main__":
	server = API()
	server.start()    