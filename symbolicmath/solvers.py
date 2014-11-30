from symbolicmath import core
import symbolicmath as sm


def to_expression(equality):
    return equality.replace("==","-(") + ")"


def solve_single_equality(equality, variable):
    expression = to_expression(equality)
    c = eval(expression, {variable: 1j})
    return {variable: -c.real/c.imag}


def solve(system):
    variable = system._generator.gi_code.co_varnames[1:][0]
    return solve_single_equality(system._expression, variable)


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
    return sm.Object(coefficient_matrix)