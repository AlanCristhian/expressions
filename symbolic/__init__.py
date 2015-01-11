"""A module that let you define functions with generator expressions."""
from symbolic import core


class Any(core.BaseType):
    """The most generic type."""
    def __setitem__(self, key, value):
        return self._array.__setitem__(key, value)

    def __repr__(self):
        return 'Any(%s)' % repr(self._array)


class System(core.BaseType):
    """A class that wrap a generator that have an system of
    equalities."""

    @helpers.cached_property
    def _expression(self):
        obj = super()._make_expression()
        return '|'.join(o._expression for o in obj) if hasattr(obj, '__iter__') \
        else obj._expression

    def __setitem__(self, key, value):
        return self._array.__setitem__(key, value)

    def __repr__(self):
        return 'System(%s)' % repr(self._array)