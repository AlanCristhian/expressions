import unittest

from expressions import solvers
import expressions as ex


class TestCoefficientMatrix(unittest.TestCase):
    @unittest.skip('Not yet implemented')
    def test_coefficient_matrix(self):
        system = ex.System(
            -x1  + 2*x2  - 3*x3  == 4  |
            5*x1 - 6*x2  + 7*x3  == -8 |
            9*x1 + 10*x2 - 11*x3 == 12
                for x1, x2, x3 in ex.Object)
        expected = ex.Object([
            [-1, 2, -3, 4],
            [5, -6, 7, -8],
            [9, 10, -11, 12]])
        obtained = solvers.extract_coefficients(system)
        self.assertEqual(obtained, expected)


class TestSolver(unittest.TestCase):
    def solve_single_variable_linear_equation(self):
        expr = ex.System(
            x - 2*x + 5*x - 46*(235-24) == x + 2 for x in ex.Object)
        result = solvers.solve(expr)
        self.assertEqual(result, {'x': 3236.0})


if __name__ == '__main__':
    unittest.main()
