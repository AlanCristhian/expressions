import re
import itertools as it

from symbolic import core


def get_independent_term_vector(expression_list, var_names):
    vector = []
    for expression in expression_list:
        for var in var_names:
            expression = expression.replace(var, '0')
        vector.append(eval(expression))
    return vector


def expanded_coefficients_matrix(system):
    # make a list of equalities
    equalities = system.expression if type(system.expression) is list \
        else [system.expression]
    # transform each equality in an expression
    expression_list = [item.expression.replace("==","-(") + ")" for item in equalities]
    # the list of names of each variable
    var_names = system._generator.gi_code.co_varnames[1:]

    N = len(var_names)
    identity_matrix = \
        [['1' if i == j else '0' for i in range(N)] for j in range(N)]

    indepentent_terms = get_independent_term_vector(expression_list, var_names)

    coeff_column_expr = []
    for expression,independent_term in zip(expression_list, indepentent_terms):
        coeff_row_expr = []
        for row in identity_matrix:
            coeff_expr = expression
            for value, name in zip(row, var_names):
                coeff_expr = coeff_expr.replace(name, value)
            coeff_row_expr.append(coeff_expr + '-%s' % independent_term)
        coeff_row_expr.append('-%s' % independent_term)
        coeff_column_expr.append(coeff_row_expr)

    # Make and return the expanded coefficients matrix
    return [[eval(item) for item in row] for row in coeff_column_expr]


# Thanks to Martin Thoma
# http://martin-thoma.com/solving-linear-equations-with-gaussian-elimination/
def gaussian_elimination(A):
    n = len(A)

    for i in range(0, n):
        # Search for maximum in this column
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k

        # Swap maximum row with current row (column by column)
        for k in range(i, n+1):
            A[i][k], A[maxRow][k] = A[maxRow][k], A[i][k]

        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            c = -A[k][i]/A[i][i]
            for j in range(i, n+1):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]

    # Solve equation Ax=b for an upper triangular matrix A
    x = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = A[i][n]/A[i][i]
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return x



def solve(system):
    # get name of each variables
    var_name = system._generator.gi_code.co_varnames[1:]
    M = expanded_coefficients_matrix(system)
    # solve the system
    x = gaussian_elimination(M)
    # Make and return a dict with that contains the name of each solution
    # with their respective value
    result = [core.BinaryRelation(name, '==', value)
            for name, value in zip(var_name, x)]
    return result[0] if len(result) == 1 else result


def get_expression_list(expression):
    pattern = re.compile('''
    (
        -[a-zA-Z0-9\*\/\.]+     # A MINUS character folowed by letters,
                                # numbers, asterisc, backslash and point.

        |\+[a-zA-Z0-9\*\/\.]+   # A PLUS character folowed by letters,
                                # numbers, asterisc, backslash and point.

        |==                     # the equality operator
    )''', re.VERBOSE)
    without_spaces = expression.replace(' ', '')
    splitted = pattern.split(without_spaces)
    filtered = filter(None, splitted)
    return list(filtered)


# TODO: replace the comparisson operator string with an object that
# represente such operator.
