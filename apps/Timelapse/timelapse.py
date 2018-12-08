import asyncio
from tornado import web
from apps.PiCam.piCam import piCam

class Timelapse:
    def __init__(self):
        self.status = 'Down'
        self.loop_flag = False

    def start(self):
        print('starting timelapse')
        self.status = 'Running'
        self.loop_flag = True
        self.start_timelapse()

    def stop(self):
        print('stopping timelapse')
        self.status = 'Down'
        self.loop_flag = False

    def start_timelapse(self, interval):
        while self.loop_flag:
            piCam.take_picture()
            time.sleep(interval)

timelapse = Timelapse()

class TimelapseStatus(web.RequestHandler):
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



class TimelapseStop(web.RequestHandler):
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



class TimelapseStart(web.RequestHandler):
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


  
