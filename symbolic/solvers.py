from symbolic import core
import symbolic as sm
import functools as ft


def to_expression(equality):
    return equality.replace("==","-(") + ")"


def solve_single_equality(expression, variable):
    c = eval(expression, {variable: 1j})
    return {variable: -c.real/c.imag}


def extract_independent_term(expression, varnames):
    for var in varnames:
        expression = expression.replace(var, '0')
    return eval(expression)


def coefficients_matrix(system):
    equalities = system._expression.split('|')
    expression_list = [to_expression(equality) for equality in equalities]
    varnames = system._generator.gi_code.co_varnames[1:] # variabe name list

    # The below code make a identity matrix
    N = len(varnames)
    identity_matrix = \
        [['1' if i == j else '0' for i in range(N)] for j in range(N)]

    indepentent_terms = [
        extract_independent_term(e, varnames) for e in expression_list]

    coeff_column_expr = []
    b = []
    for expression,independent_term in zip(expression_list, indepentent_terms):
        coeff_row_expr = []
        for row in identity_matrix:
            coeff_expr = expression
            for value, name in zip(row, varnames):
                coeff_expr = coeff_expr.replace(name, value)
            coeff_row_expr.append(coeff_expr + '-%s' % independent_term)
        coeff_row_expr.append('-%s' % independent_term)
        coeff_column_expr.append(coeff_row_expr)

    coefficient_matrix = [
        [eval(item) for item in row]
        for row in coeff_column_expr]

    return coefficient_matrix


def gauss(A):
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
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp

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

    # A is the coeficcient matrix and b is the vector of independent terms
    # Ax = b
    M = coefficients_matrix(system)

    x = gauss(M)

    result = {name: value for name, value in zip(var_name, x)}

    return result