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


def expanded_coefficients_matrix(system):
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


# Gaussian elimination algorithm by Isaac Evans.
# github.com/ievans/GaussianElimination/blob/master/gaussianelimination.py

def myGauss(m):
    # eliminate columns
    for col in range(len(m[0])):
        for row in range(col+1, len(m)):
            r = [(rowValue * (-(m[row][col] / m[col][col])))
                for rowValue in m[col]]
            m[row] = [sum(pair) for pair in zip(m[row], r)]
    # now backsolve by substitution
    ans = []
    m.reverse() # makes it easier to backsolve
    for sol in range(len(m)):
        if sol == 0:
            ans.append(m[sol][-1] / m[sol][-2])
        else:
            inner = 0
            # substitute in all known coefficients
            for x in range(sol):
                inner += (ans[x]*m[sol][-2-x])
            # the equation is now reduced to ax + b = c form
            # solve with (c - b) / a
            ans.append((m[sol][-1]-inner)/m[sol][-sol-2])
    ans.reverse()
    return ans



def solve(system):
    # get name of each variables
    var_name = system._generator.gi_code.co_varnames[1:]

    # M is the expanded coefficient matrix: M = A|b
    M = expanded_coefficients_matrix(system)

    x = myGauss(M)

    result = {name: value for name, value in zip(var_name, x)}

    return result