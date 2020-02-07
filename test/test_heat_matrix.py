import unittest
import numpy as np
from apps.Vision.HeatMatrix import HeatMatrix

class TestHeatMatrix(unittest.TestCase):

    def test_shape(self):
        classification_queue = HeatMatrix(2,5)

        self.assertEqual(classification_queue.shape, (2,2))

    def test_heat_matrix_size(self):
        self.assertRaises(Exception, HeatMatrix(1,2))
    
    def test_heat_matrix_ones(self):
        classification_queue = HeatMatrix(2,5)
        self.assertTrue(
            (classification_queue.heat_matrix == np.ones((2,2))).all())

    def test_queue_size(self):
        classification_queue = HeatMatrix(2,5)
        
        self.assertEqual(classification_queue.frames_queue.qsize(), 5)
    
    def test_heat_matrix(self):
        classification_queue = HeatMatrix(2,5)
        new_frame = np.random.rand(2,2)

        classification_queue.compute_vector(new_frame)
        self.assertTrue((classification_queue.heat_matrix == new_frame).all())

    def test_get_old_frame(self):
        classification_queue = HeatMatrix(2,5)
        old_frame = np.random.rand(2,2)

        classification_queue.compute_vector(old_frame)
        for i in range(4):
            classification_queue.compute_vector(np.random.rand(2,2))

        self.assertTrue(
            (classification_queue._get_oldest_frame() == old_frame).all())

if __name__ == '__main__':
    unittest.main()
