from tornado import web
from apps.Timelapse.timelapse import timelapse

class Status(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @web.asynchronous
    def get(self):
        # Include when the last image was taken so that users can confirm 
        # this feature is working.
        try:
            self.write({
                'service':'Timelapse',
                'status':timelapse.status})
            self.finish()
        except:
            print('Error Writing Request Response')
    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()



class Stop(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @web.asynchronous
    def get(self):  
        timelapse.stop()
        try:
            self.write({
                'service':'timelapse',
                'action':'Killing'})
            self.finish()
        except:
            print('Error Writing Request Response')
 
    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()



class Start(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @web.asynchronous
    def get(self):  
        timelapse.start()
        try:
            self.write({
                'service':'timelapse',
                'action':'Starting'})
            self.finish()
        except:
            print('Error Writing Request Response')
    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()

class SetInterval(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @web.asynchronous
    def get(self):  
        try:
            val = self.get_argument('val')
            timelapse.interval = int(val)
            self.write({
                'service':'timelapse',
                'action':'Changing Interval',
                'value': timelapse.interval})
            self.finish()
        except:
            print('Error Writing Request Response')

    @web.asynchronous 
    def options(self):
        self.set_status(204)
        self.finish()


 
