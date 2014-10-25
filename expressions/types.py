"""A library that define numeric sets."""


__all__ = ['Natural']


class NumberMeta(type):
    """A metaclass that define mathematical operators for the class."""
    def __init__(cls, name, bases, namespace):
        return super().__init__(name, bases, namespace)

    def __pow__(cls, exponent):
        """Make an N-vector with N = exponent"""
        assert isinstance(exponent, int)
        assert exponent > 0
        return cls([0 for i in range(0, exponent)])


class _NaturalVector(metaclass=NumberMeta):
    """Add `ℕ**n` interface for vector definition. Do that by the 
    NumberMeta.__pow__() method. E.g.:
    >>> v = Natural**3
    >>> v
    Natural([0, 0, 0])
    """
    def __init__(self, argument):
        if type(argument) is list:
            self._array = argument
            self._vector = True

    def __getitem__(self, arg):
        return self._array.__getitem__(arg)

    def __repr__(self):
        return 'Natural(%s)' % repr(self._array)


class _NaturalMatrix(_NaturalVector):
    """Add `ℕ**M*N` interface for matrix definition. Do that by the 
    _NaturalMatrix.__mul__() method. E.g.:
    >>> A = Natural**3*3
    >>> A
    Natural([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    """

    def __mul__(self, multiplicant):
        """Make an MxN matrix with M row an N columns where N = multiplicant
        only if cls is an N-vector."""
        assert self._vector is True
        assert type(multiplicant) is int
        assert multiplicant > 0
        return _NaturalVector([self._array for j in range(0, multiplicant)])


class Natural(_NaturalMatrix):
    ...