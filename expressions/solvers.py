from expressions import core


class System(core.BaseType):
    """The most generic type."""
    def __setitem__(self, key, value):
        return self._array.__setitem__(key, value)

    def __repr__(self):
        return 'System(%s)' % repr(self._array)


def solve(system):
    variable = system._generator.gi_code.co_varnames[1:][0]
    expression = system._expression.replace("==","-(") + ")"
    c = eval(expression, {variable: 1j})
    return {variable: -c.real/c.imag}