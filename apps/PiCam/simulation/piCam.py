import numpy
from PIL import Image
import pathlib
from apps.ImageService.imageService import imageService
from apps.Pixhawk.pixhawk import pixhawk


class PiCam:
    def __init__(self):
        self.status = "unset status"
        self.counter = 0
        pathlib.Path("home/pi/images/").mkdir(parents=True, exist_ok=True)

    def take_picture(self):
        imarray = numpy.random.rand(100, 100, 3) * 255
        im = Image.fromarray(imarray.astype("uint8")).convert("RGBA")
        fpath = "home/pi/images/" + str(self.counter) + ".png"
        im.save(fpath)
        self.counter += 1
        print(pixhawk.get_location())
        img = {
            "id": self.counter,
            "image": fpath,
            "telemetry": pixhawk.get_location(),
        }
        imageService.appendImageQueue(img)
        print("Camera Simulating Image Capture")

    def take_corrupt_pic(self):
        corrupt_pic_path = "home/pi/images/corrupt.jpg"
        imageService.appendImageQueue(corrupt_pic_path)


# Export singleton
piCam = PiCam()
