import unittest
from expressions.types import *


class TestObjectType(unittest.TestCase):
    def test_Object_vector(self):
        v = Object([0, 0, 0])
        self.assertEqual(v._array, [0, 0, 0])

    def test_Object_repr_method(self):
        v = Object([0, 0, 0])
        self.assertEqual(repr(v), 'Object([0, 0, 0])')

    def test_Object_vector_interface(self):
        """Should define a 3-vector of numbers"""
        u = Object**3;
        self.assertEqual(u._array, Object([0, 0, 0])._array)

    def test_Object_matrix(self):
        A = Object([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test_Object_matrix_interface(self):
        A = Object**3*3
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test_Object_matrix_getitem(self):
        A = Object([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        item = A[1][2]
        self.assertEqual(item, 6)

    def test_three_dimensions_Object_matrix_interface(self):
        A = Object**3*3*2
        array = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ]
        self.assertEqual(A._array, array)

    def test_setitem(self):
        v = Object**3
        v[1] = 555
        self.assertEqual(v._array, [0, 555, 0])


if __name__ == '__main__':
    unittest.main()