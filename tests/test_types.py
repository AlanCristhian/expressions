import unittest

from expressions.types import _TypeMaker, _argument_sender, _CallableMaker


class Test_TypeMakerType(unittest.TestCase):
    def test__TypeMaker_vector(self):
        v = _TypeMaker([0, 0, 0])
        self.assertEqual(v._array, [0, 0, 0])

    def test__TypeMaker_vector_interface(self):
        """Should define a 3-vector of numbers"""
        u = _TypeMaker**3;
        self.assertEqual(u._array, _TypeMaker([0, 0, 0])._array)

    def test__TypeMaker_matrix(self):
        A = _TypeMaker([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test__TypeMaker_matrix_interface(self):
        A = _TypeMaker**3*3
        array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(A._array, array)

    def test__TypeMaker_matrix_getitem(self):
        A = _TypeMaker([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        item = A[1][2]
        self.assertEqual(item, 6)

    def test_three_dimensions__TypeMaker_matrix_interface(self):
        A = _TypeMaker**3*3*2
        array = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ]
        self.assertEqual(A._array, array)


class FunctionTest(unittest.TestCase):
    def test__argument_sender(self):
        """The coroutine object created with _argument_sender should
        yield the value sended and return the value again in the next
        iteration."""
        sender = _argument_sender()
        next(sender)
        a = sender.send(2)
        b = next(sender)
        self.assertEqual(a, 2)
        self.assertEqual(b, 2)

    def test__CallableMaker(self):
        double = _CallableMaker(2*x for x in _CallableMaker)
        self.assertEqual(8, double(4))


if __name__ == '__main__':
    unittest.main()