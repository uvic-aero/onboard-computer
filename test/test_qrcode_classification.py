import unittest
import cv2
import numpy as np

from apps.Vision.QRClassification.QRCodeClassification import QRCodeClassification


class TestQRCodeClassification(unittest.TestCase):



    def test_parameters_defaults():
        """
        Instatiate class and check parameters are not none
        Defaults are whats in the config
        """
        test_config = {
            sub_image_dim: "", 
            max_height: "", 
            min_height: "", 
            max_vertices: "", 
            min_vertices: "", 
            threshold_val: "", 
            threshold_type: "", 
            contour_mode: "", 
            contour_method: "", 
            epsilon_factor: "", 
            poly_closed: ""
        }
        QR_classification = QRCodeClassification(resolution=(1080,1440))
        QR_classification.config = test_config

        pass
    
    def test_set_subimage_dim():
        """
        Assert that the LCD of the resolution dimensions is used as the
        subimage dimension.
        """
        pass

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
        clsfn = QRCodeClassification()


        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            contour
        )
        pass

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
        clsfn = QRCodeClassification()


        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            None
        )
        pass

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
        clsfn = QRCodeClassification()

        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            None
        )
        pass

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
        clsfn = QRCodeClassification()


        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            contour
        )
        pass

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
        clsfn = QRCodeClassification()


        self.assertEquals(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len),
            None
        )
        pass

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
        clsfn = QRCodeClassification()


        self.assertEquals(type(clsfn.filter_contour(
            contour=contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len)),
            np.ndarray
        )
        pass

    def test_get_contour_areas():
        """
        assert correct datatype, irrelevant contours are filtered out
        """
        max_height = 100
        min_height = 2
        max_len = 100
        min_len = 2

        # Square contour with length 4, and height 5
        valid_contour = np.asarray([
            [0, 1], [1, 4],
            [0, 0], [1, 0]
        ])

        non_valid_contour = np.asarray([
            [0, 1], [1, 1],
            [0, 0], [1, 0]
        ])
        clsfn = QRCodeClassification()

        #check type
        self.assertEquals(type(clsfn.get_contour_areas(
            contour=valid_contour, min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len)),
            np.ndarray
        )
        #check invalid gets filtered out
        self.assertEquals(clsfn.get_contour_areas(
            contour=[valid_contour, non_valid_contour], min_height=min_height, max_height=max_height, max_len=max_len, min_len=min_len).shape[0],
            valid_contour
        )
        pass

    def test_split_frames():
        """
        assert returns correct number of subimages
        """
        subimage = cv2.imread("test/assets/test_subimage_1.jpg")
        clsfn = QRCodeClassification()
        sub_images = clsfn.split_frames(subimage)
        height, width, ____ = subimage.shape

        self.assertEquals()
        pass


if __name__ == '__main__':
    unittest.main()
