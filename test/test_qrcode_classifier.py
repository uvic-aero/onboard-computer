from apps.Vision.QRClassifier.QRCodeClassifier import QRCodeClassifier


class TestQRCodeClassifier(unittest.TestCase):
    def __init__(self):
        self.test_config = {
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

    def test_get_qrcode_locations():
    """
    Pass an image, assert that return is heatmap which was the same shape as config variable sub_image dims
    """

        pass

    def test_valid_cd():
    """
    
    """


        pass



if __name__ == '__main__':
    unittest.main()