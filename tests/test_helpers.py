import unittest

from expressions import helpers


class Test_set_name(unittest.TestCase):
    def test_name_function(self):
        class A:
            def __init__(self):
                self.__name__ = helpers.get_name()

        object_name = A()
        self.assertEqual(object_name.__name__, 'object_name')


if __name__ == '__main__':
    unittest.main()