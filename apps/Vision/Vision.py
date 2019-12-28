from apps.Vision.Capture import Capture
from apps.Vision.DropOffZoneClassifier import DropOffZoneClassifier
from apps.Vision.LightSourceFinder import LightSourceFinder
from apps.Vision.QRCodeBoxClassifier import QRCodeBoxClassifier


class Vision:

    def __init__(self):
        self.Capture = Capture()
        self.DropOffZoneClassifier = DropOffZoneClassifier()
        self.LightSourceFinder = LightSourceFinder()
        self.QRCodeBoxClassifier = QRCodeBoxClassifier()
