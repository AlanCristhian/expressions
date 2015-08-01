import re
import itertools as it

from symbolic import core


def get_independent_term_vector(expression_list, var_names):
    vector = []
    N = len(expression_list)
    M = len(var_names)
    D = N - M
    for expression in expression_list:
        for i in range(M):
            expression = expression.replace(var_names[i], '0')
        if D:
            unknown = {name: core.Expression(name) for name in
                       var_names[D:]}
            vector.append(eval(expression, None, unknown))
        else:
            vector.append(eval(expression))
    return vector


def get_expressions_and_operators(relations):
    expression_list, operator_list = [], []
    for item in relations:
        if "==" in item.__expr__:
            operator_list.append(core.Eq)
            expression_list.append(item.__expr__.replace("==","-(") + ")")
        elif "!=" in item.__expr__:
            operator_list.append(core.Ne)
            expression_list.append(item.__expr__.replace("!=","-(") + ")")
        elif "<=" in item.__expr__:
            operator_list.append(core.Le)
            expression_list.append(item.__expr__.replace("<=","-(") + ")")
        elif "<"  in item.__expr__:
            operator_list.append(core.Lt)
            expression_list.append(item.__expr__.replace("<","-(")  + ")")
        elif ">=" in item.__expr__:
            operator_list.append(core.Ge)
            expression_list.append(item.__expr__.replace(">=","-(") + ")")
        elif ">"  in item.__expr__:
            operator_list.append(core.Gt)
            expression_list.append(item.__expr__.replace(">","-(")  + ")")
        else:
            raise ValueError("The expression should be an system of "
                             "equation or inequation or a mix of bot.")
    return expression_list, operator_list


def expanded_coefficients_matrix(system):
    # make a list of equalities
    relations = system.__expr__ if type(system.__expr__) is list \
        else [system.__expr__]

    # transform each equality in an expression
    expression_list, operator_list = get_expressions_and_operators(relations)

    # the list of names of each variable
    var_names = system._generator.gi_code.co_varnames[1:]

    M = len(var_names)
    N = len(expression_list)
    D = N - M

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

    if D > 0:
        unknown = {name: core.Expression(name) for name in var_names[D:]}
        # Make and return the expanded coefficients matrix
        result = [[eval(item, None, unknown) for item in row]
                   for row in coeff_column_expr]
    else:
        # Make and return the expanded coefficients matrix
        result = [[eval(item) for item in row] for row in coeff_column_expr]
    return result, operator_list


def gaussian_elimination(system, len=len, range=range, zip=zip,
                         sum=sum):
    # Size of the system
    M = len(system[0])
    N = len(system)

    # a copy of the original system
    matrix = system[:]

    # eliminate columns
    for i in range(M):
        for j in range(i + 1, N):
            row = (-system[j][i]/system[i][i]*value for value in system[i])
            matrix[j] = [x + y for x, y in zip(system[j], row)]

    # Solve equation Ax=b for an upper triangular matrix A
    result = [None for i in range(N)]
    for i in range(N-1, -1, -1):
        result[i] = matrix[i][N]/matrix[i][i]
        for k in range(i-1, -1, -1):
            matrix[k][N] -= matrix[k][i] * result[i]
    return result


def solve(system):
    # get name of each variables
    var_name = system._generator.gi_code.co_varnames[1:]
    matrix, original_operators = expanded_coefficients_matrix(system)
    # solve the system
    x = gaussian_elimination(matrix)

    operators = [r*o for r, o in zip(x, original_operators)]
    # Make and return a dict with that contains the name of each solution
    # with their respective value
    result = [op(name, value) for name, value, op in
              zip(var_name, x, operators)]
    return result[0] if len(result) == 1 else result
