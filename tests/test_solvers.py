import unittest

from expressions import solvers
import expressions as ex


class TestNatural(unittest.TestCase):
    def test_natural_argument(self):
        expr = solvers.System(
            x - 2*x + 5*x - 46*(235-24) == x + 2 for x in ex.Object)
        result = solvers.solve(expr)
        self.assertEqual(result, {'x': 3236.0})


if __name__ == '__main__':
    unittest.main()
