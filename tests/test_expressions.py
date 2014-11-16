import unittest

import expressions as ex


class TestNatural(unittest.TestCase):
    @unittest.skip('Not yet implemented')
    def test_natural_argument(self):
        function = ex.Object(x*2 for x in ex.Natural)
        value = function(2)
        result = next(value)



if __name__ == '__main__':
    unittest.main()