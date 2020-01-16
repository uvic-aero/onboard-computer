import unittest
from apps.Vision.QRClassification.QRCodeClassification import QRCodeClassification


class TestVision(unittest.TestCase):

    def test_filter_contour(self):
        clsfn = QRCodeClassification()

        self.assertEquals(clsfn.filter_contour(None), None)


if __name__ == '__main__':
    unittest.main()
