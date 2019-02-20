from tornado import web
from apps.PiCam.piCam import piCam 

#All other handlers are a copy of status handler. Change others, but not this one.
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

class TakePicture(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.take_picture()
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

class StartVideo(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.start_video()
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

class StopVideo(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.stop_video()
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

class StartPreview(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.start_preview()
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

class StopPreview(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.stop_preview()
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
        
class GetExposureCompensation(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.get_exposure_compensation()
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

class SetExposureCompensation(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        val = self.get_argument('val')
        piCam.set_exposure_compensation(val)
        print(val)
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

class IncExposureCompensation(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.inc_exposure_compensation(val)
        print(val)
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

class DecExposureCompensation(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.dec_exposure_compensation()
        print(val)
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

class GetShutterSpeed(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.get_shutter_speed()
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

class SetShutterSpeed(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        val = self.get_argument('val')
        piCam.set_shutter_speed(val)
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

class IncShutterSpeed(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.inc_shutter_speed()
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

class DecShutterSpeed(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.dec_shutter_speed()
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

class GetAwbMode(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.get_awb_mode()
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


class SetAwbMode(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        val = self.get_argument('val')
        piCam.set_awb_mode(val)
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

class GetAwbGains(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.get_awb_gains()
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

class SetAwbGains(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        val = self.get_argument('val')
        piCam.set_awb_gains(val)
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

class IncAwbGains(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.inc_awb_gains()
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

class DecAwbGains(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.dec_awb_gains()
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

class GetIso(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.get_iso()
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

class SetIso(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        val = self.get_argument('val')
        piCam.set_iso(val)
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

class IncIso(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):
        piCam.inc_iso()
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

class DecIso(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    @web.asynchronous
    def get(self):

        piCam.dec_iso()
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


