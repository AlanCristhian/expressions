import unittest

import symbolic as sm


class TestNatural(unittest.TestCase):
    @unittest.skip('Not yet implemented')
    def test_natural_argument(self):
        function = sm.Object(x*2 for x in sm.Natural)
        value = function(2)
        result = next(value)



if __name__ == '__main__':
    unittest.main()