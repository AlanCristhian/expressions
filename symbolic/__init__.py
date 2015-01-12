"""A module that let you define functions with generator expressions."""
from symbolic import core


class Any(core.MatrixType):
    """The most generic type."""
    def __setitem__(self, key, value):
        return self._array.__setitem__(key, value)

    def __repr__(self):
        return 'Any(%s)' % repr(self._array)


class System(core.CallableObject):
    """A class that wrap a generator that have an system of
    equalities."""
    def __init__(self, system, *args, **kwds):
        super().__init__(system, *args, **kwds)
        self._expression = super()._make_expression()

    def __setitem__(self, key, value):
        return self._array.__setitem__(key, value)

    def __repr__(self):
        return 'System(%s)' % repr(self._array)