from QRCodeClassification import QRCodeClassification
import numpy as np


class QRCodeBoxTraining(QRCodeClassification):
    """
    This is a class for training and scoring QR Code classifiers

    Attributes: 
        List of Float Lists: X (features)
        Integer List: Y (Labels)
    """

    def __init__(self):
        subimages = self.get_training_subimages("")
        self.X, self.Y = self.prep_training_data(subimages)

    def get_training_subimages(self, directory):
        """ 
        reads in training jpg images into a list of frames

        Parameters: 
            String: directory

        Returns: 
            List of 2D numpy arrays: Subimages
        """
        return []

    def shuffle_data(self, X, Y):
        """ 
        Shuffles training documents

        Parameters: 
            List of Float Lists: X (features)
            Integer List: Y (Labels)

        Returns: 
            Tuple of a List of Float Lists and an Integer List: 
            X (features), Y (Labels)
        """

        return ([], [])

    def prep_training_data(self, subimages):
        """ 
        processes training data into feature - label (X,Y) structure for classification

        Parameters: 
            List of 2D numpy array: subimages

        Returns: 
            Tuple of a List of Float Lists and an Integer List: 
            X (features), Y (Labels)
        """
        return ([], [])

    ''' 
    trains on training data, returns classifier
    '''

    def evaluate(self, X, Y, clsf):
        """ 
        evaluates classifier by training and testing on training data

        Parameters: 
            Parameters: 
            List of Float Lists: X (features)
            Integer List: Y (Labels)
            Sklearn Classifier object: classifier

        Returns: 
            Float: classifier score 
            2D numpy array: confusion matrix
        """
        return (0.0, np.asarray([]))

    def evaluate_classifier_algorithms(self):
        """ 
        Evaluates training data on the following classification algorithms:
            Gaussian Naive Bayes
            Logistic Regression
            Decision Tree
        and outputs results

        """
        pass
