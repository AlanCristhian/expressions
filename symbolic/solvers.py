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


def extract_coefficients(system):
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
    for expression, independent_term in zip(expression_list, indepentent_terms):
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


def to_upper_triangular(matrix):
    N = len(matrix)
    for j in range(N): # for each column on the main diag
        if matrix[j][j] == 0: # Find a non-zero pivot and swap rows 
            column = [matrix[k][j] for k in range(j, N)]
            ipivot = column.index(max(column))
            temp = matrix[j]
            matrix[j] = matrix[ipivot]
            matrix[ipivot] = temp
        for i in range(j + 1, N):
            # Ratio of (i,j) elt by (j,j) (diagonal) elt
            c = matrix[i][j]/matrix[j][j] 
            matrix[i] = \
                [matrix[i][k] - c*matrix[j][k] for k in range(N)]
    return matrix


def solve(system):
    # get name of each variables
    var_name = system._generator.gi_code.co_varnames[1:][0]
    coefficient_matrix = extract_coefficients(system)
    T = to_upper_triangular(coefficient_matrix)
    x = [core.ExpressionString(i) for i in 
        system._generator.gi_code.co_varnames[1:]]
    x.append(1)
    w = [sum(i*j for i, j in zip(row, x) if i != 0) for row in T]
    i = len(w)-2
    result = {}
    r =  [var_name] if type(var_name) is str else var_name[:]
    r[i] = solve_single_equality(w[i]._expression, var_name[i])[var_name[i]]
    i -= 1
    while i >= 0:
        expr = w[i]
        number = solve_single_equality(expr, var_name[i])[var_name[i]]
        result.update({var_name[i]: number})
        i -= 1
    return result