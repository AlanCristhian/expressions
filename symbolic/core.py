"""A library with base classes and metaclasses that let define
numeric sets."""

import inspect

from . import helpers


# Make an AST with the generator expression
# =========================================

# Python have the ast module. This library have the ast.parse(source) funtion
# that parse the source into an AST node, where source is an string. See the
# example:
# >>> y = (x*y for (x, y) in range(2))
# To reuse the ast.parse funtion I need to extract the 'x*y' string from the
# generator object.


def binary_left_operator(template):
    def decorator(function):
        def operator(self, other):
            result = ExpressionString()
            if hasattr(other, '_expression'):
                result._expression = template % \
                    (self._expression, other._expression)
            else:
                result._expression = template % \
                    (self._expression, repr(other))
            return result
        return operator
    return decorator


def binary_right_operator(template):
    def decorator(function):
        def operator(self, other):
            result = ExpressionString()
            if hasattr(other, '_expression'):
                result._expression = template % \
                    (other._expression, self._expression)
            else:
                result._expression = template % \
                    (repr(other), self._expression)
            return result
        return operator
    return decorator


def unary_operator(template):
    def decorator(function):
        def operator(self):
            result = ExpressionString()
            result._expression = template % self._expression
            return result
        return operator
    return decorator


# !!!: maybe exists an better way to implement this behaviour
class ExpressionString:
    """All magick methods make an string."""
    def __init__(self, name=None):
        if name is not None:
            self._expression = name

    def __repr__(self):
        return self._expression

    @binary_left_operator('%s+(%s)')
    def __add__(self, other):
        pass

    @binary_left_operator('%s&(%s)')
    def __and__(self, other):
        pass

    @binary_left_operator('%s/(%s)')
    def __div__(self, other):
        pass

    @binary_left_operator('%s==(%s)')
    def __eq__(self, other):
        pass

    @binary_left_operator('%s//(%s)')
    def __floordiv__(self, other):
        pass

    @binary_left_operator('%s>=(%s)')
    def __ge__(self, other):
        pass

    @binary_left_operator('%s>(%s)')
    def __gt__(self, other):
        pass

    @binary_left_operator('%s<=(%s)')
    def __le__(self, other):
        pass

    @binary_left_operator('%s<<(%s)')
    def __lshift__(self, other):
        pass

    @binary_left_operator('%s<(%s)')
    def __lt__(self, other):
        pass

    @binary_left_operator('%s@(%s)')
    def __matmul__(self, other):
        pass

    @binary_left_operator('%s%%(%s)')
    def __mod__(self, other):
        pass

    @binary_left_operator('%s*(%s)')
    def __mul__(self, other):
        pass

    @binary_left_operator('%s!=(%s)')
    def __ne__(self, other):
        pass

    @binary_left_operator('%s|(%s)')
    def __or__(self, other):
        pass

    @binary_left_operator('%s**(%s)')
    def __pow__(self, other):
        pass

    @binary_left_operator('%s>>(%s)')
    def __rshift__(self, other):
        pass

    @binary_left_operator('%s-(%s)')
    def __sub__(self, other):
        pass

    @binary_left_operator('%s/(%s)')
    def __truediv__(self, other):
        pass

    @binary_left_operator('%s^(%s)')
    def __xor__(self, other):
        pass

    # --------------------------------

    @binary_right_operator('(%s)+%s')
    def __radd__(self, other):
        pass

    @binary_right_operator('(%s)&%s')
    def __rand__(self, other):
        pass

    @binary_right_operator('(%s)/%s')
    def __rdiv__(self, other):
        pass

    @binary_right_operator('(%s)//%s')
    def __rfloordiv__(self, other):
        pass

    @binary_right_operator('(%s)<<%s')
    def __rlshift__(self, other):
        pass

    @binary_right_operator('(%s)@%s')
    def __rmatmul__(self, other):
        pass

    @binary_right_operator('(%s)%%%s')
    def __rmod__(self, other):
        pass

    @binary_right_operator('(%s)*%s')
    def __rmul__(self, other):
        pass

    @binary_right_operator('(%s)|%s')
    def __ror__(self, other):
        pass

    @binary_right_operator('(%s)**%s')
    def __rpow__(self, other):
        pass

    @binary_right_operator('(%s)>>%s')
    def __rrshift__(self, other):
        pass

    @binary_right_operator('(%s)-%s')
    def __rsub__(self, other):
        pass

    @binary_right_operator('(%s)/%s')
    def __rtruediv__(self, other):
        pass

    @binary_right_operator('(%s)^%s')
    def __rxor__(self, other):
        pass

    # --------------------------------

    @unary_operator('~(%s)')
    def __invert__(self):
        pass

    @unary_operator('-(%s)')
    def __neg__(self):
        pass

    @unary_operator('+(%s)')
    def __pos__(self):
        pass


# Make a vector
# =============

# Supose that I wish to define a vector with the below sintax:
# >>> v = Any**3
# The upper expression mean that `v` is a 3-vector with Any numbers. The 
# VectorMeta metaclass add this feature to the `Any` class through
# the `VectorMeta.__pow__()` method.

class VectorMeta(type):
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


# Make a function with the generator expression
# =============================================

# I want to define a function that do type checking of arguments and values
# returned. All those with generator-expressions. E.g:

# >>> double = Any(2*x for x in Any)
# >>> double(4)
# 8

# How I can implement this thing?


# The argument_sender() coroutine-object will be store the values passed
# with the .send() method. I will use this values as function arguments later.
# Then yield the value like a producer.

def argument_sender():
    value = None
    while True:
        # If I not yield the value, the following line return the None value.
        # This value can cause some problems inside the generator expression.
        value = yield value
        yield value


# Second, to build the generator-expression, Python3 need that the
# expression-list in the for statement in the generator-expression have the
# .__iter__() method. This method should return an iterable. The IterableMeta
# metaclass do that.

class IterableMeta(type):
    """Make a class that is an iterable object."""
    def __new__(cls, name, bases, namespace):
        return super().__new__(cls, name, bases, namespace)

    def __iter__(cls):
        # !!!: the iter method return the argument_sender() coroutine-object
        sender = argument_sender()
        next(sender)
        return sender


# Join IterableMeta and VectorMeta
class IterableAndVectorMeta(IterableMeta, VectorMeta):
    pass



# Variables with the .__name__ property
# =====================================

class NamedObject:
    """Make an object with the __name__ property."""
    def __init__(self):
        self._name = helpers.get_name()

    def _get_outer_globals(self, frame):
        """Yield all global variables in the higher (calling) frames.
        """
        while frame:
            yield frame.f_globals
            frame = frame.f_back

    # NOTE: I define the __name__ property as a method because I need to store
    # the name after object creation. The @helpers.cached_property decorator
    # call the __name__ method and then transform itself into a property.
    @helpers.cached_property
    def __name__(self):
        """Find the name of the instance of the current class.
        Then store it in the .__name__ attribute."""
        # NOTE: If you use this class in the interactive IDLE shell, the 
        # `helpers.get_name()` function return `None`. So, I find the name of
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
    def __init__(self, generator, name, args):
        self._generator = generator
        self._expression = name + repr(args).replace(',)', ')')

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

    @helpers.cached_property
    def gi_running(self):
        return self._generator.gi_running

    def __repr__(self):
        return self._expression


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
        return the object with the "_expression" property."""
        # CAVEAT: everything the first var name in gi_code.co_varnames is "0.0"
        # This is the name of the iterator used in the first *for* statement
        # in the generator.
        expr_obj = self(*(ExpressionString(name)
            for name in self._generator.gi_code.co_varnames[1:]))
        return next(expr_obj)

    @helpers.cached_property
    def _expression(self):
        obj = self._make_expression()
        return obj._expression if hasattr(obj, '_expression') \
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


class BaseType(MatrixType):
    """A class that have all shared behaviours of all numeric types."""
