import unittest

from symbolic import lazymatrix as lm


@unittest.skip('not work yet')
class traverse_Test(unittest.TestCase):
    def test_get_shape(self):
        l = [[1, 2, 5], [3, 4, 6]]
        obtained = lm._get_shape(l)
        expected = (2, 3)
        self.assertEqual(expected, obtained)

@unittest.skip('not work yet')
class MatrixTest(unittest.TestCase):
    def test_Matrix_instance(self):
        A = lm.Matrix()
        self.assertTrue(isinstance(A, lm.Matrix))

    def test_column_creation(self):
        c = lm.Matrix([1, 2])
        self.assertEqual(c[0], 1)
        self.assertEqual(c[1], 2)


if __name__ == '__main__':
    unittest.main()