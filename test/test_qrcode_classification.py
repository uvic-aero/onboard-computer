import unittest
import cv2
import numpy as np

from apps.Vision.QRClassification.QRCodeClassification import QRCodeClassification


class TestQRCodeClassification(unittest.TestCase):

    def __init__(self):
        self.test_config = {
            sub_image_dim: (216, 216),
            max_height: 1900,
            min_height: 20,
            max_vertices: 50,
            min_vertices: 2,
            threshold_val: 120,
            epsilon_factor: 0.05,
            poly_closed: True
        }
        self.res = resolution = (1080, 1440)

    def test_parameters_defaults():
        """
        Instatiate class and check parameters are not none
        Defaults are whats in the config
        """
        QR_classification = QRCodeClassification(self.res)
        QR_classification.config = self.test_config

    def test_exract_features(self):
        """
            Assert exract_features returns a list 
            of 3 non-zero floats
        """
        subimage = cv2.imread("test/assets/test_subimage_1.jpg")
        clsfn = QRCodeClassification(self.res)
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
        clsfn = QRCodeClassification(self.res)

        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            None
        )

    def test_filter_contour_gt_min_lt_max_ht():
        """
        positive case, inbetween the two bounds
        """
        max_height = 100
        min_height = 2
        max_len = 100
        min_len = 2

        # Square contour with length 4, and height 5
        contour = np.asarray([
            [0, 1], [1, 4],
            [0, 0], [1, 0]
        ])
        clsfn = QRCodeClassification(self.res)

        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            contour
        )

    def test_filter_countour_gt_max_ht():
        """
        negative case, exceeds upper bound
        """
        max_height = 100
        min_height = 2
        max_len = 100
        min_len = 2

        # Square contour with length 4, and height 100000
        contour = np.asarray([
            [0, 1], [1, 100000],
            [0, 0], [1, 0]
        ])
        clsfn = QRCodeClassification(self.res)

        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            None
        )

    def test_filter_countour_vertice_lt_min():
        """
        negative case, vertices less than lower bound
        """
        max_height = 100
        min_height = 2
        max_len = 100
        min_len = 2

        # Square contour with length 1, and height 1
        contour = np.asarray([
            [0, 1]
        ])
        clsfn = QRCodeClassification(self.res)

        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            None
        )

    def test_filter_countour_vertice_gt_min_lt_max():
        """
        positive case, vertices is within bounds
        """
        max_height = 100
        min_height = 2
        max_len = 100
        min_len = 2

        # Square contour with length 4, and height 5
        contour = np.asarray([
            [0, 1], [1, 4],
            [0, 0], [1, 0]
        ])
        clsfn = QRCodeClassification(self.res)

        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            contour
        )

    def test_filter_countour_vertice_gt_max():
        """
        negative case, vertices exceeds upper bound
        """
        max_height = 100
        min_height = 2
        max_len = 10
        min_len = 2

        # Square contour with length 12, and height 5
        contour = np.asarray([
            [0, 1], [1, 4],
            [0, 0], [1, 0],
            [1, 1], [0, 4],
            [1, 3], [0, 3],
            [2, 1], [2, 4],
            [0, 2], [2, 0]
        ])
        clsfn = QRCodeClassification(self.res)

        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            None
        )

    def test_extract_contours():
        """
        assert that correct datatype is returned
        """
        max_height = 100
        min_height = 2
        max_len = 100
        min_len = 2

        # Square contour with length 4, and height 5
        contour = np.asarray([
            [0, 1], [1, 4],
            [0, 0], [1, 0]
        ])
        clsfn = QRCodeClassification(self.res)

        self.assertEquals(type(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len)),
            np.ndarray
        )

    def test_get_contour_areas():
        """
        correct areas are returned.
        """
        max_height = 100
        min_height = 2
        max_len = 100
        min_len = 2

        # Square contour with length 4, and height 4
        contour_1x4_len4 = np.asarray([
            [0, 1], [1, 4],
            [0, 0], [1, 0]
        ])
        contour_2x5_len4 = np.asarray([
            [0, 1], [2, 5],
            [0, 0], [2, 0]
        ])
        contour_1x1_len4 = np.asarray([
            [0, 1], [1, 1],
            [0, 0], [1, 0]
        ])
        test_countours = [contour_1x4_len4, contour_2x5_len4, contour_1x1_len4]
        expected_areas = np.array([4.0, 10.0])
        clsfn = QRCodeClassification(self.res)

        # expect invalid areas to be filtered out
        self.assertEquals(clsfn.get_contour_areas(
            contours=test_countours, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len).shape[0],
            expected_areas
        )

    def test_split_frames():
        """
        assert returns correct number of subimages
        """
        image = cv2.imread("test/assets/test_2592x1944_image.jpg")
        height, width, ____ = image.shape
        resolution = (height, width)
        clsfn = QRCodeClassification(self.res)
        sub_images = clsfn.split_frames(image)

        num_images = (
            height / self.config.sub_image_dim[0])*(width / self.config.sub_image_dim[1])
        # check correct number of
        self.assertEquals(num_images, sub_images.shape[0])


if __name__ == '__main__':
    unittest.main()
