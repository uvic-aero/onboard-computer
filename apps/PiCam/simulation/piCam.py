import numpy
from PIL import Image
import pathlib

class PiCam:
    def __init__(self):
        self.status = 'unset status'
        self.counter = 0
        pathlib.Path('home/pi/images/').mkdir(parents=True, exist_ok=True) 
   
    def take_picture(self):
        imarray = numpy.random.rand(100,100,3) * 255
        im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')

        im.save('home/pi/images/' +  str(self.counter) + '.png')
        self.counter += 1
        print('Camera Simulating Image Capture')

# Export singleton
piCam = PiCam()

