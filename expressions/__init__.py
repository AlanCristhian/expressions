"""A module that let you define functions with generator expressions."""
from expressions import core


class Object(core.BaseType):
    """The most generic type."""
    def __setitem__(self, key, value):
        return self._array.__setitem__(key, value)

    def __repr__(self):
        return 'Object(%s)' % repr(self._array)
