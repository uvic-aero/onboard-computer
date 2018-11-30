import asyncio
from tornado import web

class ImageService:
    def __init__(self):
        self.img_path = '~/obc/images/'
        self.status = 'down'

    # The start and stop functions do not need to be used if the programmer 
    # thinks that this class should not take the form of a process

    def start(self):
        #this function is responsible for inidtializing connections 
        #and processes that may be used by the ImageService class
        self.status = 'maybe running'
        pass

    def stop(self):
        self.status = 'down'
        pass
    
    def save_img(self, img):
        # this function will receive an image and store it locally
        # with telemetry data(hopefully inside photo metadata).
        pass
 
    def get_telemetry(self):
        # this function probes telem2 port on pixhawk for gps data
        pass

    def send_img(self, img):
        # this function must send images to
        # the ground station in the form of a post request
        # refer to apps/SonyCamera/stillProcessor.py for example
        # 1. encode img in base 64
        # 2. add gps data and encoded image to dict 
        # 3. requests.post(groundstation_url + '/images', json=payload)
        pass

imageService = ImageService()


class ImageServiceStatus(web.RequestHandler):
    @web.asynchronous
    def get(self):
        try:
            self.write({
                'service':'ImageService',
                'status':imageService.status})
            self.finish()
        except:
            print('Error Writing Request Response')


class ImageServiceStop(web.RequestHandler):
    @web.asynchronous
    def get(self):  
        imageService.stop()
        try:
            self.write({
                'service':'imageService',
                'action':'Killing'})
            self.finish()
        except:
            print('Error Writing Request Response')

class ImageServiceStart(web.RequestHandler):
    @web.asynchronous
    def get(self):  
        imageService.start()
        try:
            self.write({
                'service':'imageService',
                'action':'Starting'})
            self.finish()
        except:
            print('Error Writing Request Response') 
