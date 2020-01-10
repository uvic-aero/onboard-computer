from QRCodeClassification import QRCodeClassification


class QRCodeClassifier(QRCodeClassification):
    """
    This is a class for classifying images containing QR codes

    Attributes: 
        SKlearn classifier object: clsf
    """

    def __init__(self):
        self.clsf = self.load_clsf_from_pickle_file("")

    def load_clsf_from_pickle_file(self, fname):
        """ 
        loads trained classification object from pickle file

        Parameters: 
            String: fname

        Returns: 
            SKlearn classifier object: clsf
        """
        return None

    def get_QR_code_locations(self, image):
        """
        calculates a list of the highest probability subimages for containing QR codes

        Parameters: 
            2D numpy array: image, 
            [[(x11,y11), ... , (x1n,y1n)], [(x21,y21), ... , (x2n,y2n)]]

        Returns:
            List of real number tuples: list of (x,y,p), where x and y are the pixel coordinate
            of the center of a subimage containing a QR code, and p is the probability of
            that subimage containing a QR code 
        """

    def classify(self, subimage):
        """ 
        Classifies subimages as containing a QR codes or not containing
        a QR Code 

        Parameters: 
            2D numpy array: Subimage

        Returns: 
            Mixed tuple: (Boolean) Classification, (Float) Probability
        """
        return False
