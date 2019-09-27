from tornado import web
from apps.ImageService.imageService import imageService


class Status(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")

    @web.asynchronous
    def get(self):
        try:
            self.write({"service": "ImageService", "status": imageService.status})
            self.finish()
        except:
            print("Error Writing Request Response")

    @web.asynchronous
    def options(self):
        self.set_status(204)
        self.finish()


class Stop(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")

    @web.asynchronous
    def get(self):
        imageService.stop()
        try:
            self.write({"service": "imageService", "action": "Killing"})
            self.finish()
        except:
            print("Error Writing Request Response")

    @web.asynchronous
    def options(self):
        self.set_status(204)
        self.finish()


class Start(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")

    @web.asynchronous
    def get(self):
        imageService.start()
        try:
            self.write({"service": "imageService", "action": "Starting"})
            self.finish()
        except:
            print("Error Writing Request Response")

    @web.asynchronous
    def options(self):
        self.set_status(204)
        self.finish()
