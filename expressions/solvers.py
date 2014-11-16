from expressions import core


def solve_single_equality(equality, variable):
    expression = equality.replace("==","-(") + ")"
    c = eval(expression, {variable: 1j})
    return {variable: -c.real/c.imag}


def solve(system):
    variable = system._generator.gi_code.co_varnames[1:][0]
    return solve_single_equality(system._expression, variable)


def extract_coefficients(system):
    print(system._expression)
    # equalities = system._expression.split('|')
    # equality 
