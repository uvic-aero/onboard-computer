from tornado import web
from apps.PiCam.piCam import piCam 

class Status(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        try:
            self.write({
                'service':'PiCam',
                'status':piCam.status})
            self.finish()
        except:
            print('Error Writing Request Response')
    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()

