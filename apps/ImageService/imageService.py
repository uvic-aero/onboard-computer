import asyncio
from tornado import web
import time
import base64
import requests
from threading import Thread, Lock
from time import sleep

from apps.Config.config import config

class ImageService:

    groundstation_url = config.values['groundstation']['ip'] + ':' + config.values['groundstation']['port']

    def __init__(self):
        self.img_path = '~/obc/images/'
        self.status = 'down'
        self.image_queue = []
        self.mutex = Lock()
        self.poll_time = config.values['imageService']['poll_time']


    # The start and stop functions do not need to be used if the programmer 
    # thinks that this class should not take the form of a process

    def start(self):
        #this function is responsible for inidtializing connections 
        #and processes that may be used by the ImageService class
        # self.status = 'maybe running'
        print('starting imageService')
        image_queue_thread = Thread(target = self.poll_image_queue, args=(self.poll_time,))
        image_queue_thread.start()

    # poll_time is the amount of time in seconds that the thread sleeps in between
    # checking the queue if there is an image ready to be sent to groundstation
    def poll_image_queue(self, poll_time):
        while True: 
            self.mutex.acquire()
            img_to_send = self.peekImageQueue()
            if img_to_send is not None:
                encoded_img_to_send = self.get_encoded_img(img_to_send)
                if encoded_img_to_send is not None:
                    if self.send_img(encoded_img_to_send):
                        self.popImageQueue() 
                else:
                    self.popImageQueue()    
            self.mutex.release()    
            sleep(poll_time)            

    # test function to put images in the queue
    def add_new_image_to_queue(self, add_time):
        x = 0
        while True:
            self.appendImageQueue('photo' + str(x%3 + 1) + '.jpg')        
            x += 1
            sleep(add_time)
    
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

    # returns Encoded image given filename
    # returns None if image couldn't be opened
    def get_encoded_img(self, img):
        try: 
            with open(img, 'rb') as image_file:
                return base64.b64encode(image_file.read())
        except Exception as e:
            print(str(e))
            print("Failed to get encoded image. Removing '" + str(img) + "' from queue.")  
            return None   

    # accepts encoded image 
    # returns True if image successfully sent to groundstation
    def send_img(self, encoded_img):
        timestamp = time.time() * 1000
        try:
            payload = {
                'timestamp': timestamp,
                'image': encoded_img.decode('utf-8', "ignore")
            }
            requests.post(self.groundstation_url + '/images', json=payload)
            print('successfully sent image to the groundstation.')
            return True
        except Exception as e:
            print(str(e))
            print("Failed to send image to groundstation")
            return False
        # File pointer

        # this function must send images to
        # the ground station in the form of a post request
        # refer to apps/SonyCamera/stillProcessor.py for example
        # 1. encode img in base 64
        # 2. add gps data and encoded image to dict 
        # 3. requests.post(groundstation_url + '/images', json=payload)
        # pass
    
    # protects queue mutex
    # add an image to the Image queue
    def appendImageQueue(self, img):
        self.mutex.acquire()
        self.image_queue.append(img)
        self.mutex.release()

    # protects queue mutex
    # return an image from the top of the queue
    def popImageQueue(self):
        return self.image_queue.pop(0)
    
    # protects queue mutex
    # returns None if queue is empty
    def peekImageQueue(self):
        head = None
        if self.image_queue:
            head = self.image_queue[0]
            
        return head

imageService = ImageService()



