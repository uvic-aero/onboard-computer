import asyncio
from tornado import web

# Create an async HTTP Client that can take in images and send them to the GroundStation
class image_service:
    def __init__(self):
        pass
    def start(self):
        # this function will at least initialize a window for the user to see the picam.
        pass

    def stop(self):
        # this function should kill the camera viewing window and 
        # any other processes it has started.
        pass

    def check_status(self):
        # check all possible processes that may not be working properly, make sure they return
        # expected values.
        # return list of broken services.
        pass


class image_serviceStatus(web.RequestHandler):
    @web.asynchronous
    def get(self):
        try:
            self.write({
                'service':'image_service',
                'status':'broken'})
            self.finish()
        except:
            print('Error Writing Request Response')

# Export a singleton accessible from camera/liveview classes
image_service = image_service()