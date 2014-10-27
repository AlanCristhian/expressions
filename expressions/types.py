"""A library that define numeric sets."""


__all__ = ['Object']


# Supose that I wish to define a vector with the below sintax:
# >>> v = Object**3
# The upper expression mean that `v` is a 3-vector with Object numbers. The 
# _VectorMakerMeta metaclass add this feature to the `Object` class through
# the `_VectorMakerMeta.__pow__()` method.

class _VectorMakerMeta(type):
    """Add `NumericType**N` API interface for to make an N-vector with
    components of `NumericType` type.
    """
    def __init__(cls, name, bases, namespace):
        return super().__init__(name, bases, namespace)

    def __pow__(cls, exponent):
        """Make an N-vector of `cls` type with N = `exponent`."""
        assert type(exponent) is int
        assert exponent > 0

        return cls([0 for i in range(0, exponent)])


# Now supose that I wish to define a matrix with the sintax:
# >> A = Object**3*4
# The `A` object is a matrix with 3 rows and 4 columns. The
# `_MatrixMaker.__mul__()` method set such feature to the object created
# with the `Object**3` expression. In te example `Object` is an subclass of
# `_MatrixMaker`.

class _MatrixMaker(metaclass=_VectorMakerMeta):
    """Add `NumericType**M*N` API interface to make an MxN matrix with
    components of `NumericType`type.
    """
    def __init__(self, argument):
        self._array = argument

    def __getitem__(self, arg):
        return self._array.__getitem__(arg)

    def __mul__(self, multiplicant):
        assert type(multiplicant) is int
        assert multiplicant > 0

        return _MatrixMaker([self._array for j in range(0, multiplicant)])


class _TypeMaker(_MatrixMaker):
    """A class that have all shared behaviours of all numeric types."""


class Object(_TypeMaker):
    """The most generic type."""
    def __setitem__(self, key, value):
        return self._array.__setitem__(key, value)

    def __repr__(self):
        return 'Object(%s)' % repr(self._array)
