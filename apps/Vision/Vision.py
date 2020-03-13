from apps.Vision.DropOffZoneClassifier import DropOffZoneClassifier
from apps.Vision.LightSourceFinder import LightSourceFinder
from apps.Vision.QRClassification.QRCodeClassifier import QRCodeClassifier
from apps.Vision.HeatMatrix import HeatMatrix
from apps.PiCam.piCam import piCam
import cv2
import time


class Vision:

    def __init__(self):
        self.DropOffZoneClassifier = DropOffZoneClassifier()
        self.LightSourceFinder = LightSourceFinder()
        self.QRCodeClassifier = QRCodeClassifier()
        self.HeatMatrix = HeatMatrix(2, 5)

    def start(self):
        while True:
            piCam.capture()  # returns numpy frame
    '''
    #TEST WEBCAM VIDEO
            cv2.imshow("Image", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
    '''


vision = Vision()
