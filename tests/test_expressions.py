import unittest
import collections
import dis

import expressions


class TestOject(unittest.TestCase):

    def test_minimal_object_function(self):
        function = expressions.Object(x for x in expressions.Object)
        self.assertEqual(function(2), 2)


    def test__find_arguments_classes(self):
        e = expressions.Object(x for x in expressions.Object)
        expected = [(object,)]
        obtained = e._arguments_classes
        self.assertEqual(expected, obtained)


if __name__ == '__main__':
    unittest.main()