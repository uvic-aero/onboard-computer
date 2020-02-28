import unittest
import numpy as np
from apps.Vision.HeatMatrix import HeatMatrix
from apps.Vision.HeatMatrix import ValueTooSmallError, InvalidOriginError

class TestHeatMatrix(unittest.TestCase):

    def test_shape(self):
        HM = HeatMatrix(2,5)

        self.assertEqual(HM.shape, (2,2))

    def test_heat_matrix_size(self):
        with self.assertRaises(ValueTooSmallError) as cm:
            HeatMatrix(1,2)
    
    def test_heat_matrix_ones(self):
        HM = HeatMatrix(2,5)
        self.assertTrue(
            (HM.heat_matrix == np.ones((2,2))).all())

    def test_queue_size(self):
        HM = HeatMatrix(2,5)
        
        self.assertEqual(HM.frames_queue.qsize(), 5)
    
    def test_new_frame(self):
        HM = HeatMatrix(2,5)
        new_frame = np.random.rand(2,2)

        HM.compute_vector(new_frame)
        self.assertTrue((HM.heat_matrix == new_frame).all())

    def test_old_frame(self):
        HM = HeatMatrix(2,5)
        old_frame = np.random.rand(2,2)

        HM.compute_vector(old_frame)
        for i in range(4):
            HM.compute_vector((old_frame + i ))

        self.assertTrue(
            (HM._get_oldest_frame() == old_frame).all())
        
    def test_origin_default(self):
        size = 2
        HM = HeatMatrix(size,5)
        origin = np.array([size/2,size/2])

        self.assertTrue(
            (HM.origin == origin).all())

    def test_origin_custom(self):
        origin = np.array([0,1])
        HM = HeatMatrix(2,5,origin=origin)

        self.assertTrue(
            (HM.origin == origin).all())

    def test_invalid_custom_origin(self):
        with self.assertRaises(InvalidOriginError) as cm:
            origin = np.array([2,2])
            HeatMatrix(2,5, origin=origin)

    def test_compute_vector_default_origin(self):
        HM = HeatMatrix(3,5)
        
        new_frame = np.zeros((3,3))
        max_cord = np.array([0,2])
        new_frame[max_cord[0]][max_cord[1]] = 1
        vector = HM.compute_vector(new_frame)

        self.assertTrue(
            (vector == (HM.origin - max_cord)).all())

    def test_compute_vector_custom_origin(self):
        origin = np.array([0,1])
        HM = HeatMatrix(3,5,origin=origin)
        
        new_frame = np.zeros((3,3))
        max_cord = np.array([0,2])
        new_frame[max_cord[0]][max_cord[1]] = 1
        vector = HM.compute_vector(new_frame)
        
        self.assertTrue(
            (vector == (HM.origin - max_cord)).all())

if __name__ == '__main__':
    unittest.main()
