"""A module that let you define functions with generator expressions."""
from symbolicmath import core


class Object(core.BaseType):
    """The most generic type."""
    def __setitem__(self, key, value):
        return self._array.__setitem__(key, value)

    def __repr__(self):
        return 'Object(%s)' % repr(self._array)


class System(core.BaseType):
    """A class that wrap a generator that have an system of
    equalities."""
    def __setitem__(self, key, value):
        return self._array.__setitem__(key, value)

    def __repr__(self):
        return 'System(%s)' % repr(self._array)