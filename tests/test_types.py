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


    def test_three_dimensions_Natural_matrix_interface(self):
        A = Natural**3*3*2
        array = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ]
        self.assertEqual(A._array, array)


if __name__ == '__main__':
    unittest.main()