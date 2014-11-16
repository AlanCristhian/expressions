import unittest

from symbolicmath import lazymatrix as lm


class DictVectorTest(unittest.TestCase):
    def test_vector_initialization(self):
        v = lm.DictVector([1, 2, 3])
        self.assertEqual(v.vector, [1, 2, 3])

    def test_void_vector(self):
        v = lm.DictVector()
        self.assertEqual(v.vector, None)

    def test_get_item(self):
        v = lm.DictVector([4, 5, 6])
        item = v[1]
        self.assertEqual(item, 5)
        self.assertEqual(v.stored, {1: 5})

    def test_get_all_items(self):
        v = lm.DictVector([7, 8, 9])
        [v[i] for i in range(3)]
        self.assertEqual(v.stored, {0: 7, 1: 8, 2: 9})
        self.assertFalse(hasattr(v, 'vector'))

    def test_set_item(self):
        v = lm.DictVector([7, 8, 9])
        v[4] = 0
        self.assertTrue(0 in v.values())

    @unittest.skip('Not yet implemented')
    def test_item_in_vector(self):
        v = lm.DictVector([1, 2, 3])
        v[4] = 0
        self.assertTrue(1 in v.values())

    @unittest.skip('Not yet implemented')
    def test_vector_repr(self):
        v = lm.DictVector([1, 2, 3])
        self.assertEqual(repr(v), '[1, 2, 3]')

if __name__ == '__main__':
    unittest.main()