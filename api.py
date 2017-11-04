import tornado.ioloop
import tornado.web
# An HTTP server that will receive commands from the GroundStation
class API:
    
	def __init__(self):
		self.routes = [(r"/", MainHandler),
		(r"/STILL", TakePicture)]
		

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
		#TODO: Call Capture Function on Camera
		
		
#TODO: Create template for all required functions


#For Debugging Use (Running Independantly for now):
if __name__ == "__main__":
	server = API()
	server.start()


    