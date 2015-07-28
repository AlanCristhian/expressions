import re
import itertools as it

from symbolic import core


def get_independent_term_vector(expression_list, var_names):
    vector = []
    N = len(expression_list)
    M = len(var_names)
    D = N - M
    for expression in expression_list:
        for i in range(N):
            expression = expression.replace(var_names[i], '0')
        if D:
            unknown = {name: core.Expression(name) for name in
                       var_names[D:]}
            vector.append(eval(expression, None, unknown))
        else:
            vector.append(eval(expression))
    return vector


def expanded_coefficients_matrix(system):
    # make a list of equalities
    equalities = system.__expr__ if type(system.__expr__) is list \
        else [system.__expr__]

    # transform each equality in an expression
    expression_list, operator_list = [], []
    for item in equalities:
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
            raise ValueError("The expression shoud be an system of equalities "
                             "or inequalities or a mix of bot.")

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

    if D:
        unknown = {name: core.Expression(name) for name in
                   var_names[D:]}
        # Make and return the expanded coefficients matrix
        result = [[eval(item, None, unknown) for item in row]
                   for row in coeff_column_expr]
    else:
        # Make and return the expanded coefficients matrix
        result = [[eval(item) for item in row]
                   for row in coeff_column_expr]
    return result, operator_list

def gaussian_elimination(system, len=len, range=range, zip=zip,
                         sum=sum):
    # Size of the system
    M = len(system[0])
    N = len(system)
    matrix = system[:]

    # eliminate columns
    for i in range(M):
        for j in range(i + 1, N):
            row = (-system[j][i]/system[i][i]*value for value in system[i])
            matrix[j] = [x + y for x, y in zip(system[j], row)]

    # now backsolve by substitution
    result = []

    # makes it easier to backsolve
    matrix.reverse()
    for j in range(N):
        if j == 0:
            result.append(matrix[j][-1] / matrix[j][-2])
        else:

            # substitute in all known coefficients
            inner = sum(result[x]*matrix[j][-2 - x] for x in range(j))

            # the equation is now reduced to ax + b = c form
            # solve with (c - b) / a
            result.append((matrix[j][-1] - inner)/matrix[j][-j - 2])

    result.reverse()
    return result


def solve(system):
    # get name of each variables
    var_name = system._generator.gi_code.co_varnames[1:]
    M, original_operators = expanded_coefficients_matrix(system)
    # solve the system
    x = gaussian_elimination(M)

    operators = [r*o for r, o in zip(x, original_operators)]
    # Make and return a dict with that contains the name of each solution
    # with their respective value
    result = [op(name, value) for name, value, op in
              zip(var_name, x, operators)]
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
