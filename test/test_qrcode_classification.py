import unittest
import cv2
import numpy as np

from apps.Vision.QRClassification.QRCodeClassification import QRCodeClassification


class TestVision(unittest.TestCase):

    def test_exract_features(self):
        """
            Assert exract_features returns a list 
            of 3 non-zero floats
        """
        subimage = cv2.imread("test/assets/test_subimage_1.jpg")
        clsfn = QRCodeClassification()
        features = clsfn.exract_features(subimage)

        self.assertEqual(len(features), 3)
        for feat in features:
            self.assertGreater(feat, 0.0)
            self.assertIsInstance(feat, float)

    def test_filter_contour_lt_min_height(self):
        """
            Asserts that contour is less than min height
        """
        max_height = 100
        min_height = 2
        max_len = 100
        min_len = 2

        # Square contour with length 4, and height 1
        contour = np.asarray([
            [0, 1], [1, 1],
            [0, 0], [1, 0]
        ])
        clsfn = QRCodeClassification()

        self.assertEquals(clsfn.filter_contour(
            contour=contour, max_height=max_height, max_len=max_len, min_len=min_len),
            None
        )


if __name__ == '__main__':
    unittest.main()
