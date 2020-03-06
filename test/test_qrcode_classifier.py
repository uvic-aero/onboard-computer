from apps.Vision.QRClassifier.QRCodeClassifier import QRCodeClassifier


class TestQRCodeClassifier(unittest.TestCase):
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

    def test_get_qrcode_locations():
        """
        Pass an image, assert that return is heatmap which was the same shape as config variable sub_image dims
        """
        image = cv2.imread("test/assets/test_2592x1944_image.jpg")
        clsfn = QRCodeClassifier(self.res)
        self.assertEqual(clsfn.get_qrcode_locations(
            image).shape, self.config.sub_image_dim)

    def test_classify():
        """
        Pass a subimage, assert that it returns probability score
        """
        subimage = cv2.imread("test/assets/test_subimage_1.jpg")
        clsfn = QRCodeClassifier(self.res)
        self.assertIsInstance(clsfn.classify(
            subimage), float)


if __name__ == '__main__':
    unittest.main()
