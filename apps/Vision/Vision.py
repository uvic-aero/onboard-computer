from Capture import Capture
from DropOffZoneClassifier import DropOffZoneClassifier
from LightSourceFinder import LightSourceFinder
from QRCodeBoxClassifier import QRCodeBoxClassifier


class Vision:

    def __init__(self):
        self.Capture = Capture()
        self.DropOffZoneClassifier = DropOffZoneClassifier()
        self.LightSourceFinder = LightSourceFinder()
        self.QRCodeBoxClassifier = QRCodeBoxClassifier()
