import asyncio
from tornado import web
import time
import base64
import requests

class ImageService:
    ImageQueue = []
    groundstation_url = 'http://localhost:24002'

    def __init__(self):
        self.img_path = '~/obc/images/'
        self.status = 'down'

    # The start and stop functions do not need to be used if the programmer 
    # thinks that this class should not take the form of a process

    def start(self):
        #this function is responsible for inidtializing connections 
        #and processes that may be used by the ImageService class
        # self.status = 'maybe running'
        print('starting imageService')
        
        while True:
            if ImageQueue:
                img_to_send = self.peekImageQueue()
                if self.send_img(img_to_send):

    def stop(self):
        self.status = 'down'
        print('stoping imageService')
        pass
    
    def save_img(self, img):
        # this function will receive an image and store it locally
        # with telemetry data(hopefully inside photo metadata).
        pass
 
    def get_telemetry(self):
        # this function probes telem2 port on pixhawk for gps data
        pass

    # image is the current string
    def send_img(self, img):
        try:
            timestamp = time.time() * 1000
            with open(img, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read())

            payload = {
                'timestamp': timestamp,
                'image': encoded_image.decode('utf-8', "ignore")
            }
            requests.post(groundstation_url + '/images', json=payload)

        except Exception as e:
            print(str(e))
            print("Failed to send image to groundstation")
        # File pointer

        # this function must send images to
        # the ground station in the form of a post request
        # refer to apps/SonyCamera/stillProcessor.py for example
        # 1. encode img in base 64
        # 2. add gps data and encoded image to dict 
        # 3. requests.post(groundstation_url + '/images', json=payload)
        # pass
    
    # add an image to the Image queue
    def appendImageQueue(self, img):
        self.ImageQueue.append(img)

    # return an image from the top of the queue
    def popImageQueue(self, img):
        return self.ImageQueue.pop()
    
    def peekImageQueue(self, img):
        try 
            return self.ImageQueue[-1]
        except Exception as e:
            print(str(e))


imageService = ImageService()



