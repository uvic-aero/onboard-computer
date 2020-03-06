class QRCodeClassification:

    def __init__(self):

        # initialize config
        config = {
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
        pass

    def exract_features(self, subimage):
        """ 
        Extracts the following subimage countour features: 
            * Mean area of all contours 
            * Standard Deviation of area of all contours
            * Cardinality of contours (number of contours)

        Parameters: 
            2D numpy array: Subimage

        Returns: 
            List: [mean_area, std_area, cardinality_of_contour]
        """
        return [0.0, 0.0, 0.0]

    def filter_contour(self, contour):
        """ 
        filter out contours that are too small or too large
        returns contour if valid

        Parameters: 
            List of numpy arrays: Contour, [(x1,y1), ... , (xn,yn)] 

        Returns: 
            List: [mean_area, std_area, cardinality_of_contour]
        """
        return []

    def extract_countours(self, subimage):
        """ 
        extracts contours from subimage

        Parameters: 
            2D numpy array: subimage

        Returns: 
            List of Lists of numpy arrays: Contours, 
            [[(x11,y11), ... , (x1n,y1n)], [(x21,y21), ... , (x2n,y2n)]] 
        """
        return []

    def get_contour_areas(self, contours):
        """ 
        computes area of each contour, filters irrelevant areas

        Parameters: 
            List of Lists of numpy arrays: Contours, 
            [[(x11,y11), ... , (x1n,y1n)], [(x21,y21), ... , (x2n,y2n)]] 

        Returns: 
            Float List: Areas
        """
        return []

    def split_frames(self, image):
        """ 
        splits image into 216x216 subimages

        Parameters: 
            2D numpy array: image, 
            [[(x11,y11), ... , (x1n,y1n)], [(x21,y21), ... , (x2n,y2n)]] 

        Returns: 
            List of 2D numpy arrays: Subimages
        """
        return []
