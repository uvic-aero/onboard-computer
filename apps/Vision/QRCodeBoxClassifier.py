class QRCodeBoxClassifier:

    def __init__(self):
        pass

    def filter_contour():
        pass

    '''
    reads in training jpg images into a list of frames
    returns frames
    '''

    def get_training_frames(self, directory):
        pass

    '''
    extracts contours from frame
    returns list of contours
    '''

    def extract_countours(self, frame):
        pass

    '''
    computes area of each contour, filters irrelevant areas
    returns list of areas
    '''
    def get_contour_areas():
        pass

    '''
    Extracts countour data, computes areas of each contour
    Computes the following features: mean, standard dev, and cardinality of contour areas
    returns tuple of features
    '''

    def exract_features(self, frame):
        pass

    '''
    splits image into 216x216 frames
    returns list of frames
    '''

    def split_frames(self, img):
        pass

    '''
    Shuffles training documents
    returns shuffled training documents
    '''

    def shuffle_data(self, a, b):
        pass

    '''
    processes training data into training instance - label (X,Y) structure for classification
    returns tuple of training instances and labels
    '''
    def prep_training_data():
        pass

    ''' 
    trains on training data, returns classifier
    '''

    def train(self, X, Y, clsf):
        pass

    ''' 
    Evaluates training data on Gaussian Naive Bayes
    '''

    def test_GNB(self):
        pass

    ''' 
    Evaluates training data on Logistic Regression
    '''

    def test_LogisticRegression(self):
        pass

    ''' 
    Evaluates training data on Decision Tree Classifier
    '''

    def test_DecisionTreeClassifier(self):
        pass
