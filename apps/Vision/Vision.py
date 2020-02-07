from apps.Vision.Capture import Capture
from apps.Vision.DropOffZoneClassifier import DropOffZoneClassifier
from apps.Vision.LightSourceFinder import LightSourceFinder
from apps.Vision.QRClassification.QRCodeClassifier import QRCodeClassifier
from apps.Vision.HeatMatrix import HeatMatrix


class Vision:

    def __init__(self):
        self.Capture = Capture()
        self.DropOffZoneClassifier = DropOffZoneClassifier()
        self.LightSourceFinder = LightSourceFinder()
        self.QRCodeClassifier = QRCodeClassifier()
        self.HeatMatrix = HeatMatrix()


vision = Vision()
