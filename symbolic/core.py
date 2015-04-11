"""A library with base classes and metaclasses that let medefine
numeric sets and some mathematical expressions."""


import inspect
import traceback

from symbolic import utils


"""
Get the output expression of the generator expression
=====================================================

A generator expression consists of the following parts:

- An Input Sequence.
- A Variable representing members of the input sequence.
- An Optional Predicate expression.
- An Output Expression producing elements of the output list from
  members of the Input Sequence that satisfy the predicate.

Consider the folowing example:
>>> (2*x for x in range(5) if x > 3)

The `2*x` part is the `output expression`, `x` is the variable,
`range(5)` is the `input sequence` and `if x > 3` is the
`optional predicate`.

So, I want to have an str with the `output expression` of the
`generator expression`. The code below do that.
"""


_BINARY_LEFT_OPERATOR = [
    ('__add__', '%s+(%s)'),
    ('__and__', '%s&(%s)'),
    ('__div__', '%s/(%s)'),
    ('__eq__', '%s==(%s)'),
    ('__floordiv__', '%s//(%s)'),
    ('__ge__', '%s>=(%s)'),
    ('__gt__', '%s>(%s)'),
    ('__le__', '%s<=(%s)'),
    ('__lshift__', '%s<<(%s)'),
    ('__lt__', '%s<(%s)'),
    ('__matmul__', '%s@(%s)'),
    ('__mod__', '%s%%(%s)'),
    ('__mul__', '%s*(%s)'),
    ('__ne__', '%s!=(%s)'),
    ('__or__', '%s|(%s)'),
    ('__pow__', '%s**(%s)'),
    ('__rshift__', '%s>>(%s)'),
    ('__sub__', '%s-(%s)'),
    ('__truediv__', '%s/(%s)'),
    ('__xor__', '%s^(%s)'),
]

_BINARY_RIGHT_OPERATOR = [
    ('__radd__', '(%s)+%s'),
    ('__rand__', '(%s)&%s'),
    ('__rdiv__', '(%s)/%s'),
    ('__rfloordiv__', '(%s)//%s'),
    ('__rlshift__', '(%s)<<%s'),
    ('__rmatmul__', '(%s)@%s'),
    ('__rmod__', '(%s)%%%s'),
    ('__rmul__', '(%s)*%s'),
    ('__ror__', '(%s)|%s'),
    ('__rpow__', '(%s)**%s'),
    ('__rrshift__', '(%s)>>%s'),
    ('__rsub__', '(%s)-%s'),
    ('__rtruediv__', '(%s)/%s'),
    ('__rxor__', '(%s)^%s'),
]

_UNARY_OPERATOR = [
    ('__invert__', '~(%s)'),
    ('__neg__', '-(%s)'),
    ('__pos__', '+(%s)'),
]


def _binary_left_operator(template):
    """Return a function that make an expression string with a binary
    left operator."""
    def operator(self, other):
        result = ExpressionString()
        if hasattr(other, 'expression'):
            result.expression = template % \
                (self.expression, other.expression)
        else:
            result.expression = template % \
                (self.expression, repr(other))
        return result
    return operator


def _binary_right_operator(template):
    """Return a function that make an expression string with an
    binary operator placed at the right of the variable."""
    def operator(self, other):
        result = ExpressionString()
        if hasattr(other, 'expression'):
            result.expression = template % \
                (other.expression, self.expression)
        else:
            result.expression = template % \
                (repr(other), self.expression)
        return result
    return operator


def _unary_operator(template):
    """Return a function that make an expression
    string with an unary operator."""
    def operator(self):
        result = ExpressionString()
        result.expression = template % self.expression
        return result
    return operator


class _DefineAllOperatorsMeta(type):
    """All operators of the new class will return an string that
    represent the mathematical expression."""
    def __new__(cls, name, bases, namespace):
        namespace.update({function: _binary_left_operator(template) for \
                          function, template in _BINARY_LEFT_OPERATOR})
        namespace.update({function: _binary_right_operator(template) for \
                          function, template in _BINARY_RIGHT_OPERATOR})
        namespace.update({function: _unary_operator(template) for \
                          function, template in _UNARY_OPERATOR})
        new_class = super().__new__(cls, name, bases, namespace)
        return new_class


class ExpressionString(metaclass=_DefineAllOperatorsMeta):
    """Create an symbolic variable."""
    def __init__(self, name=None):
        if name is not None:
            self.expression = name

    def __repr__(self):
        return self.expression


"""
Make a vector
=============

Supose that I want to define a vector with the below sintax:
>>> v = Real**3
The upper expression mean that `v` is a 3-vector with Real numbers. The
VectorMeta metaclass add this feature to the `Real` class through
the `VectorMeta.__pow__()` method.
"""

class VectorMeta(type):
    """Add `NumericType**N` API interface for to make an N-vector with
    components of `NumericType` type.
    """
    def __pow__(cls, exponent):
        """Make an N-vector of `cls` type with N = `exponent`."""
        assert type(exponent) is int
        assert exponent > 0

        return cls([0 for i in range(0, exponent)])


"""
Make a function with the generator expression
=============================================

I want to define a function that do type checking of arguments and values
returned. Also, I want that the the funtion to be lazy. All those with
generator-expressions. E.g:

>>> double = Real(2*x for x in Real)
>>> double(4)
double(4)
>>> next(double(4))
8

How I can implement this thing?
"""

# FIRST: The argument_sender() coroutine-object will be store the values passed
# with the .send() method. I will use this values as function arguments later.
# Then yield the value like a producer.

def argument_sender():
    value = None
    while True:
        # If I not yield the value, the following line return the None value.
        # None value can cause some problems inside the generator expression.
        value = yield value
        yield value


# SECOND, to build the generator-expression, Python3 need that the
# `input sequence` object in the generator-expression have the
# .__iter__() method. This method should return an iterable. The IterableMeta
# metaclass do that.

class IterableMeta(type):
    """Make a class that is an iterable object."""
    def __iter__(cls):
        # !!!: the iter method return the argument_sender() coroutine-object
        sender = argument_sender()
        # To get a co-routine to run properly, you have to
        # ping it with a next() operation first
        next(sender)
        return sender


class IterableAndVectorMeta(IterableMeta, VectorMeta):
    """All behaviours of IterableMeta and VectorMeta in one."""


class NamedObject:
    """Make an object with the __name__ property."""
    def __init__(self):
        self._name = self._get_name()

    def _get_name(self):
        """Find the name of the instance of the current class.
        Then store it in the .__name__ attribute."""
        *_, text = traceback.extract_stack()[-6]
        if text:
            name, *_ = text.split('=')
            return name.strip()

    def _get_outer_globals(self, frame):
        """Yield all global variables in the higher (calling) frames.
        """
        while frame:
            yield frame.f_globals
            frame = frame.f_back

    # NOTE: I define the __name__ property as a method because I need to store
    # the name after object creation. The @utils.cached_property decorator
    # call the __name__ method and then transform itself into a property.
    @utils.cached_property
    def __name__(self):
        """Find the name of the instance of the current class.
        Then store it in the .__name__ attribute."""
        # NOTE: If you use this class in the interactive IDLE shell, the
        # `utils.get_name()` function return `None`. So, I find the name of
        # the var in the global namespace of each frame.
        if self._name is None:
            global_variables = self._get_outer_globals(inspect.currentframe())
            for glob in global_variables:
                for name, value in glob.items():
                    if value is self:
                        return name
        else:
            name = self._name
            del self._name
            return name


class CalledObject:
    """This object is created when you call the the function."""
    def __init__(self, generator, name, args):
        self._generator = generator
        self.expression = name + repr(args).replace(',)', ')')

    def __iter__(self):
        return self._generator.__iter__

    def __next__(self):
        return self._generator.__next__()

    def close(self):
        return self._generator.close()

    def send(self, *args, **kwds):
        return self._generator.send(*args, **kwds)

    def throw(self):
        return self._generator.throw()

    @utils.cached_property
    def gi_running(self):
        return self._generator.gi_running

    def __repr__(self):
        return self.expression


# Third, I use the coroutine-object returned by the __iter__() method to pass
# values in each iteration of the generator expression. Such values act like
# funtions parameters. The generator-expression is an consumer.

class CallableObject(NamedObject):
    def __init__(self, generator):
        super().__init__()
        self._generator = generator
        self._send = self._generator.gi_frame.f_locals['.0'].send

    def _make_expression(self):
        """Send an ExpressionString() object to the generator. Then
        return the object with the ".expression" property."""
        # CAVEAT: everything the first var name in gi_code.co_varnames is "0.0"
        # This is the name of the iterator used in the first *for* statement
        # in the generator.
        expr_obj = self(*(ExpressionString(name)
            for name in self._generator.gi_code.co_varnames[1:]))
        return next(expr_obj)

    @utils.cached_property
    def expression(self):
        obj = self._make_expression()
        return obj.expression if hasattr(obj, 'expression') \
        else self.__name__

    def __call__(self, *args):
        """Simulate a function call."""
        # send arguments to the internal coroutine
        self._send(args[0]) if len(args) is 1 else self._send(args)

        # avance the generator and return their value
        return CalledObject(self._generator, self.__name__, args)


# Make a matrix
# =============

# Now supose that I wish to define a matrix with the sintax:
# >> A = Any**3*4
# The `A` object is a matrix with 3 rows and 4 columns. The
# `MatrixType.__mul__()` method set such feature to the object created
# with the `Any**3` expression. In te example `Any` is an subclass of
# `MatrixType`.

class MatrixType(CallableObject, metaclass=IterableAndVectorMeta):
    """Add `NumericType**M*N` API interface to make an MxN matrix with
    components of `NumericType`type.
    """
    def __init__(self, argument):
        if type(argument) is not list:
            super().__init__(argument)
        self._array = argument

    def __getitem__(self, arg):
        return self._array.__getitem__(arg)

    def __mul__(self, multiplicant):
        assert type(multiplicant) is int
        assert multiplicant > 0

        return MatrixType([self._array for j in range(0, multiplicant)])


# The below class is used to represent inequalities and equalities.
# Not to be confused with "inequation" and "equation".

class BinaryRelation:
    """Represents a binary relation between two quantities or
    expressions. For example: `x <= 2`."""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return 'BinaryRelation(%s %s %s)' % \
            (self.left, self.operator, self.right)

    def __eq__(self, other):
        if self.left == other.left \
        and self.operator == other.operator \
        and self.right == other.right:
            return True
        else:
            return False


class EqualOperator:
    def __add__(self, other):
        return other
