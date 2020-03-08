import cv2
import numpy as np
import os

class QRCodeClassification:
    resolution = (1944, 2592)   # expected resolution of image. Note .shape from cv2 could be used instead
    gridSize = 18               # common factor of image height and width, used to divide image into gridSize x Gridsize subimages

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

    def extract_features(self, subimage):
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
        contours = self.extract_countours(subimage)
        areas = self.get_contour_areas(contours)
        doc = [0.0, 0.0, 0.0]
        if len(areas) > 0:
            mean = np.mean(areas)
            std = np.std(areas)
            card = len(areas)
            doc[0] = mean
            doc[1] = std
            doc[2] = float(card)

        return doc

    def filter_contour(self, contour):
        """ 
        filter out contours that are too small or too large
        returns contour if valid

        Parameters: 
            List of numpy arrays: Contour, [(x1,y1), ... , (xn,yn)] 

        Returns: 
            List: [mean_area, std_area, cardinality_of_contour]
        """
        curve_len = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.05 * curve_len, True)
        if len(approx) >= 2 and len(approx) < 50:
            x, y, w, h = cv2.boundingRect(approx)
            if h > 20 and h < 1900:
                return (x, y)

        return None

    def extract_countours(self, subimage): 
        """ 
        extracts contours from subimage

        Parameters: 
            2D numpy array: subimage

        Returns: 
            List of Lists of numpy arrays: Contours, 
            [[(x11,y11), ... , (x1n,y1n)], [(x21,y21), ... , (x2n,y2n)]] 
        """
        gray = cv2.cvtColor(subimage, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        contours, h = cv2.findContours(
                thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    def get_contour_areas(self, contours):
        """ 
        computes area of each contour, filters irrelevant areas

        Parameters: 
            List of Lists of numpy arrays: Contours, 
            [[(x11,y11), ... , (x1n,y1n)], [(x21,y21), ... , (x2n,y2n)]] 

        Returns: 
            Float List: Areas
        """
        areas = []
        for i, cont in enumerate(contours):
            x, y = self.filter_contour(cont)
            if x > -1:
                areas.append(cv2.contourArea(cont))
        
        return areas

    def split_frames(self, image): 
        """ 
        splits image into 216x216 subimages

        Parameters: 
            2D numpy array: image, 
            [[(x11,y11), ... , (x1n,y1n)], [(x21,y21), ... , (x2n,y2n)]] 

        Returns: 
            List of 2D numpy arrays: Subimages
        """
        subimages = []
        img = cv2.imread(image)
        subimgHeight = self.resolution[0]//self.gridSize
        subimgWidth = self.resolution[1]//self.gridSize
    
        for r in range(0, self.resolution[0],  subimgHeight):
            for c in range(0, self.resolution[1], subimgWidth):
                subimages.append(img[r:r+subimgHeight, c:c+subimgWidth, :])

        return subimages
