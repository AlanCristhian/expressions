import unittest

from symbolic.solvers import system_linear_equations as solvers
from symbolic import core
import symbolic as sm


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
        system = sm.System([
             -x1 +  2*x2 -  3*x3 ==  4,
            5*x1 -  6*x2 +  7*x3 == -8,
            9*x1 + 10*x2 - 11*x3 == 12]
                for (x1, x2, x3) in sm.Any)

        expected = [[-1,  2,  -3,  4],
                    [ 5, -6,   7, -8],
                    [ 9, 10, -11, 12]]

        obtained = solvers.expanded_coefficients_matrix(system)
        self.assertEqual(obtained, expected)

    def test_unsorted_expanded_coefficients_matrix(self):
        """Should extract all coefficients of an unsorted system of linear
        equalities."""
        system = sm.System([
                      -x1 +  2*x2 ==  4 + 3*x3,
              7*x3 +  5*x1 - 6*x2 == -8,
            -11*x3 + 10*x2 + 9*x1 == 12]
                for (x1, x2, x3) in sm.Any)

        expected = [[-1,  2,  -3,  4],
                    [ 5, -6,   7, -8],
                    [ 9, 10, -11, 12]]

        obtained = solvers.expanded_coefficients_matrix(system)
        self.assertEqual(obtained, expected)


class TestSolver(unittest.TestCase):
    def test_solve_single_variable_linear_equation(self):
        expr = sm.System(
            x - 2*x + 5*x - 46*(235-24) == x + 2 for x in sm.Any)
        result = solvers.solve(expr)
        self.assertEqual(result, core.BinaryRelation('x', '==', 3236.0))

    def test_zero_equation(self):
        expr = sm.System(
            0 == x + 4 for x in sm.Any)
        result = solvers.solve(expr)
        self.assertEqual(result, core.BinaryRelation('x', '==', -4.0))

    def test_solve_system_of_3x3(self):
        system = sm.System([
             -x1 +  2*x2 -  3*x3 ==  4,
            5*x1 -  6*x2 +  7*x3 == -8,
            9*x1 + 10*x2 - 11*x3 == 12]
                for (x1, x2, x3) in sm.Any)
        r = solvers.solve(system)
        self.assertAlmostEqual(r[0].right, 0.0)
        self.assertAlmostEqual(r[1].right, -1.0)
        self.assertAlmostEqual(r[2].right, -2.0)

    @unittest.expectedFailure
    def test_solve_insonsistent_system(self):
        system = sm.System([
             -x1 + 2*x2 - 3*x3 == 4,
            5*x1 - 6*x2 + 7*x3 == -8]
                for (x1, x2, x3) in sm.Any)
        obtained = solvers.solve(system)
        expected = [core.BinaryRelation('x2', '==', '2*x1-1'),
            core.BinaryRelation('x3', '==', 'x1-2')]
        self.assertEqual(obtained, expected)


if __name__ == '__main__':
    unittest.main()
