import unittest
from expressions.types import *


class TestNaturalType(unittest.TestCase):
    def test_Natural_vector(self):
        v = Natural([0, 0, 0])
        self.assertEqual(v._array, [0, 0, 0])

    def test_Natural_repr_method(self):
        v = Natural([0, 0, 0])
        self.assertEqual(repr(v), 'Natural([0, 0, 0])')

    def test_Natural_vector_interface(self):
        """Should define a 3-vector of natural numbers"""
        u = Natural**3;
        self.assertEqual(u._array, Natural([0, 0, 0])._array)

    def test_Natural_matrix(self):
        A = Natural([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test_Natural_matrix_interface(self):
        A = Natural**3*3
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test_Natural_matrix_getitem(self):
        A = Natural([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        item = A[1][2]
        self.assertEqual(item, 6)

    def test_three_dimensions_Natural_matrix_interface(self):
        A = Natural**3*3*2
        array = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ]
        self.assertEqual(A._array, array)

    def test_setitem(self):
        v = Natural**3
        v[1] = 555
        self.assertEqual(v._array, [0, 555, 0])

    def test_error_if_set_a_non_natural_nuber(self):
        v = Natural**3
        with self.assertRaises(AssertionError):
            v[0] = 3.5
        with self.assertRaises(AssertionError):
            v[0] = 0
        with self.assertRaises(AssertionError):
            v[0] = -1


if __name__ == '__main__':
    unittest.main()