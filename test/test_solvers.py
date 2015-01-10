import unittest

from symbolic import solvers
import symbolic as sm


class TestCoefficientMatrix(unittest.TestCase):
    def test_extract_independent_term(self):
        expr = '9*x1 + 10*x2 - 11*x3 + 12'
        obtained = solvers.extract_independent_term(expr, ['x1', 'x2', 'x3'])
        expected = 12
        self.assertEqual(obtained, expected)

    def test_coefficients_matrix(self):
        system = sm.System([
             -x1  + 2*x2  - 3*x3 ==  4,
            5*x1 -  6*x2  + 7*x3 == -8,
            9*x1 + 10*x2 - 11*x3 == 12]
                for x1, x2, x3 in sm.Any)

        expected = [[-1,  2,  -3,  4],
                    [ 5, -6,   7, -8],
                    [ 9, 10, -11, 12]]

        obtained = solvers.coefficients_matrix(system)
        self.assertEqual(obtained, expected)

class TestSolver(unittest.TestCase):
    def test_solve_single_variable_linear_equation(self):
        expr = sm.System(
            x - 2*x + 5*x - 46*(235-24) == x + 2 for x in sm.Any)
        result = solvers.solve(expr)
        self.assertEqual(result, {'x': 3236.0})

    def test_zero_equation(self):
        expr = sm.System(
            0 == x + 4 for x in sm.Any)
        result = solvers.solve(expr)
        self.assertEqual(result, {'x': -4.0})

    def test_solve_system_of_3x3(self):
        system = sm.System([
            -x1  + 2*x2  - 3*x3 == 4,
            5*x1 - 6*x2  + 7*x3  == -8,
            9*x1 + 10*x2 - 11*x3 == 12]
                for x1, x2, x3 in sm.Any)
        r = solvers.solve(system)
        self.assertAlmostEqual(r['x1'], 0.0)
        self.assertAlmostEqual(r['x2'], -1.0)
        self.assertAlmostEqual(r['x3'], -2.0)


if __name__ == '__main__':
    unittest.main()
