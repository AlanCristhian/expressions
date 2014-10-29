"""A library with base classes and metaclasses that let define
numeric sets."""


# Supose that I wish to define a vector with the below sintax:
# >>> v = Object**3
# The upper expression mean that `v` is a 3-vector with Object numbers. The 
# _VectorMakerMeta metaclass add this feature to the `Object` class through
# the `_VectorMakerMeta.__pow__()` method.

class _VectorMakerMeta(type):
    """Add `NumericType**N` API interface for to make an N-vector with
    components of `NumericType` type.
    """
    def __new__(cls, name, bases, namespace):
        return super().__new__(cls, name, bases, namespace)

    def __pow__(cls, exponent):
        """Make an N-vector of `cls` type with N = `exponent`."""
        assert type(exponent) is int
        assert exponent > 0

        return cls([0 for i in range(0, exponent)])


# I want to define a function that do type checking of arguments and values
# returned. All those with generator-expressions. E.g:

# >>> double = Object(2*x for x in Object)
# >>> double(4)
# 8

# How I can implement this thing?


# The _argument_sender() coroutine-object will be store the values passed
# with the .send() method. I will use this values as function arguments later.
# Then yield the value like a producer.

def _argument_sender():
    value = None
    while True:
        # If I not yield the value, the following line return the None value.
        # This value can cause some problems inside the generator expression.
        value = yield value
        yield value


# Second, to build the generator-expression, Python3 need that the
# expression-list in the for statement in the generator-expression have the
# .__iter__() method. This method should return an iterable. The _IterableMeta
# metaclass do that.

class _IterableMeta(type):
    """Make a class that is an iterable object."""
    def __new__(cls, name, bases, namespace):
        return super().__new__(cls, name, bases, namespace)

    def __iter__(cls):
        # !!!: the iter method return the _argument_sender() coroutine-object
        sender = _argument_sender()
        next(sender)
        return sender


# Join _IterableMeta and _VectorMakerMeta
class _IterableAndVectorMeta(_IterableMeta, _VectorMakerMeta):
    pass


# Third, I use the coroutine-object returned by the __iter__() method to pass
# values in each iteration of the generator expression. Such values act like
# funtions parameters. The generator-expression is an consumer.

class _CallableMaker(metaclass=_IterableAndVectorMeta):
    def __init__(self, generator):
        self._generator = generator
        # Cache the send method of the internal coroutine. Before an
        # investigation I found that the first expression_list in the for
        # statement everything is stored in the same place:
        self._send = self._generator.gi_frame.f_locals['.0'].send

    def __call__(self, *args):
        """Simulate a function call."""
        # send arguments to the internal coroutine
        for a in args:
            self._send(a)
        # avance the generator and return their value
        return next(self._generator)


# Now supose that I wish to define a matrix with the sintax:
# >> A = Object**3*4
# The `A` object is a matrix with 3 rows and 4 columns. The
# `_MatrixMaker.__mul__()` method set such feature to the object created
# with the `Object**3` expression. In te example `Object` is an subclass of
# `_MatrixMaker`.

class _MatrixMaker(_CallableMaker):
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
