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
    equalities = system._expression if type(system._expression) is list \
        else [system._expression]
    # transform each equality in an expression
    expression_list = [item._expression.replace("==","-(") + ")" for item in equalities]
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


# Gaussian elimination algorithm by Isaac Evans.
# github.com/ievans/GaussianElimination/blob/master/gaussianelimination.py

def gaussian_elimination(m):
    # eliminate columns
    for col in range(len(m[0])):
        for row in range(col+1, len(m)):
            r = (-m[row][col] / m[col][col] * rowValue for rowValue in m[col])
            m[row] = [sum(pair) for pair in zip(m[row], r)]
    # now backsolve by substitution
    ans = []
    m.reverse() # makes it easier to backsolve
    for sol in range(len(m)):
        if sol == 0:
            ans.append(m[sol][-1] / m[sol][-2])
        else:
            # substitute in all known coefficients
            inner = sum(ans[x]*m[sol][-2-x] for x in range(sol))
            # the equation is now reduced to ax + b = c form
            # solve with (c - b) / a
            ans.append((m[sol][-1]-inner)/m[sol][-sol-2])
    ans.reverse()
    return ans


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
