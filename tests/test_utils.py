import unittest

from symbolic import utils


class Test_cached_property(unittest.TestCase):
    def setUp(self):
        class Any:
            def __init__(self):
                self.called = False
            @utils.cached_property
            def my_property(self):
                self.called = True
                return 'my_property'
        self.obj = Any()

    def test_non_getted_property(self):
        self.assertTrue('my_property' in dir(self.obj))
        self.assertFalse(self.obj.called)

    def test_getted_property(self):
        self.obj.my_property
        self.assertTrue(self.obj.called)
        self.assertEqual(self.obj.my_property, 'my_property')


if __name__ == '__main__':
    unittest.main()
