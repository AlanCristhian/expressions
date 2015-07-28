import unittest

from symbolic import solvers
from symbolic import core
import symbolic


class TestExpressionMatrix(unittest.TestCase):
    def test_get_expression_list(self):
        expression = '9*x1 + 10*x2 - 11*x3 == 12'
        obtained = solvers.get_expression_list(expression)
        expected = ['9*x1', '+10*x2', '-11*x3', '==', '12']
        self.assertEqual(obtained, expected)


class TestCoefficientMatrix(unittest.TestCase):
    def test_get_independent_term_vector(self):
        expr_list = [
            " -x1 +  2*x2 -  3*x3 -  4",
            "5*x1 -  6*x2 +  7*x3 +  8",
            "9*x1 + 10*x2 - 11*x3 - 12"]
        obtained = solvers.get_independent_term_vector(
            expr_list, ['x1', 'x2', 'x3'])
        expected = [-4, 8, -12]
        self.assertEqual(obtained, expected)

    def test_expanded_coefficients_matrix(self):
        system = symbolic.System([
             -x1 +  2*x2 -  3*x3 ==  4,
            5*x1 -  6*x2 +  7*x3 == -8,
            9*x1 + 10*x2 - 11*x3 == 12]
                for (x1, x2, x3) in symbolic.Any)

        matrix = [[-1,  2,  -3,  4],
                  [ 5, -6,   7, -8],
                  [ 9, 10, -11, 12]]
        expected = matrix, [core.Eq]*3

        obtained = solvers.expanded_coefficients_matrix(system)
        self.assertEqual(obtained, expected)

    def test_unsorted_expanded_coefficients_matrix(self):
        """Should extract all coefficients of an unsorted system of linear
        equalities."""
        system = symbolic.System([
                      -x1 +  2*x2 ==  4 + 3*x3,
              7*x3 +  5*x1 - 6*x2 == -8,
            -11*x3 + 10*x2 + 9*x1 == 12]
                for (x1, x2, x3) in symbolic.Any)

        matrix = [[-1,  2,  -3,  4],
                    [ 5, -6,   7, -8],
                    [ 9, 10, -11, 12]]
        expected = matrix, [core.Eq]*3

        obtained = solvers.expanded_coefficients_matrix(system)
        self.assertEqual(obtained, expected)


class TestSolver(unittest.TestCase):
    def test_solve_single_variable_linear_equation(self):
        expr = symbolic.System(
            x - 2*x + 5*x - 46*(235-24) == x + 2 for x in symbolic.Any)
        result = solvers.solve(expr)
        self.assertEqual(result, core.Eq('x', 3236.0))

    def test_zero_equation(self):
        expr = symbolic.System(
            0 == x + 4 for x in symbolic.Any)
        result = solvers.solve(expr)
        self.assertEqual(result, core.Eq('x', -4.0))

    def test_solve_system_of_3x3(self):
        system = symbolic.System([
             -x1 +  2*x2 -  3*x3 ==  4,
            5*x1 -  6*x2 +  7*x3 == -8,
            9*x1 + 10*x2 - 11*x3 == 12]
                for (x1, x2, x3) in symbolic.Any)
        r = solvers.solve(system)
        self.assertAlmostEqual(r[0].right, 0.0)
        self.assertAlmostEqual(r[1].right, -1.0)
        self.assertAlmostEqual(r[2].right, -2.0)

    def test_solve_inequality(self):
        system = symbolic.System(2 - 3*x < 7 for x in symbolic.Any)
        expected = core.Gt("x", -5/3)
        obtained = solvers.solve(system)
        self.assertAlmostEqual(obtained, expected)


if __name__ == '__main__':
    unittest.main()
