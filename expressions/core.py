"""A library with base classes and metaclasses that let define
numeric sets."""

import functools as ft
import itertools as it
import inspect

from . import helpers


# _BINARY_LEFT_OPERATORS = {
#     '__add__': '%s+(%s)',
#     '__and__': '%s&(%s)',
#     '__div__': '%s/(%s)',
#     '__eq__': '%s==(%s)',
#     '__floordiv__': '%s//(%s)',
#     '__ge__': '%s>=(%s)',
#     '__gt__': '%s>(%s)',
#     '__le__': '%s<=(%s)',
#     '__lshift__': '%s<<(%s)',
#     '__lt__': '%s<(%s)',
#     '__matmul__': '%s@(%s)',
#     '__mod__': '%s%%(%s)',
#     '__mul__': '%s*(%s)',
#     '__ne__': '%s!=(%s)',
#     '__or___': '%s|(%s)',
#     '__pow__': '%s**(%s)',
#     '__rshift__': '%s>>(%s)',
#     '__sub__': '%s-(%s)',
#     '__truediv__': '%s/(%s)',
#     '__xor__': '%s^(%s)',
# }

# _BINARY_RIGHT_OPERATORS = {
#     '__radd__': '(%s)+%s',
#     '__rand__': '(%s)&%s',
#     '__rdiv__': '(%s)/%s',
#     '__rfloordiv__': '(%s)//%s',
#     '__rlshift__': '(%s)<<%s',
#     '__rmatmul__': '(%s)@%s',
#     '__rmod__': '(%s)%%%s',
#     '__rmul__': '(%s)*%s',
#     '__ror___': '(%s)|%s',
#     '__rpow__': '(%s)**%s',
#     '__rrshift__': '(%s)>>%s',
#     '__rsub__': '(%s)-%s',
#     '__rtruediv__': '(%s)/%s',
#     '__rxor__': '(%s)^%s',
# }

# _UNARY_OPERATORS = {
#     '__invert__': '~(%s)',
#     '__neg__': '-(%s)',
#     '__pos__': '+(%s)',
# }

# _CALLABLE_OPERATORS = {
#     '__abs__': 'abs(%s)',
#     '__bool__': 'bool(%s)',
#     '__dir__': 'dir(%s)',
#     '__float__': 'float(%s)',
#     '__format__': 'format(%s)',
#     '__hash__': 'hash(%s)',
#     '__int__': 'int(%s)',
#     '__repr__': 'repr(%s)',
#     '__str__': 'str(%s)',
# }

# _SPECIAL_METHODS = {   
#     '__delattr__': 'delattr(%s,%s)',
#     '__divmod__': 'divmod(%s,%s)',
#     '__getattribute__': 'getattribute(%s,%s)',
#     '__rdivmod__': 'divmod(%s,%s)',
#     '__setattr__': 'setattr(%s,%s,%s)',
# }


# Make an AST with the generator expression
# =========================================

# Python have the ast module. This library have the ast.parse(source) funtion
# that parse the source into an AST node, where source is an string. See the
# example:
# >>> y = (x*y for (x, y) in range(2))
# To reuse the ast.parse funtion I need to extract the 'x*y' string from the
# generator object.


def _binary_left_operator(template):
    def decorator(function):
        def operator(self, other):
            result = _MakeExpressionString()
            if hasattr(other, '_expression'):
                result._expression = template % \
                    (self._expression, other._expression)
            else:
                result._expression = template % \
                    (self._expression, repr(other))
            return result
        return operator
    return decorator


def _binary_right_operator(template):
    def decorator(function):
        def operator(self, other):
            result = _MakeExpressionString()
            if hasattr(other, '_expression'):
                result._expression = template % \
                    (other._expression, self._expression)
            else:
                result._expression = template % \
                    (repr(other), self._expression)
            return result
        return operator
    return decorator


def _unary_operator(template):
    def decorator(function):
        def operator(self):
            result = _MakeExpressionString()
            result._expression = template % self._expression
            return result
        return operator
    return decorator


# !!!: maybe exists an better way to implement this behaviour
class _MakeExpressionString:
    """All magick methods make an string."""
    def __init__(self, name=None):
        if name is not None:
            self._expression = name

    def __repr__(self):
        return self._expression

    @_binary_left_operator('%s+(%s)')
    def __add__(self, other):
        pass

    @_binary_left_operator('%s&(%s)')        
    def __and__(self, other):
        pass

    @_binary_left_operator('%s/(%s)')        
    def __div__(self, other):
        pass

    @_binary_left_operator('%s==(%s)')        
    def __eq__(self, other):
        pass

    @_binary_left_operator('%s//(%s)')        
    def __floordiv__(self, other):
        pass

    @_binary_left_operator('%s>=(%s)')        
    def __ge__(self, other):
        pass

    @_binary_left_operator('%s>(%s)')        
    def __gt__(self, other):
        pass

    @_binary_left_operator('%s<=(%s)')        
    def __le__(self, other):
        pass

    @_binary_left_operator('%s<<(%s)')        
    def __lshift__(self, other):
        pass

    @_binary_left_operator('%s<(%s)')        
    def __lt__(self, other):
        pass

    @_binary_left_operator('%s@(%s)')        
    def __matmul__(self, other):
        pass

    @_binary_left_operator('%s%%(%s)')        
    def __mod__(self, other):
        pass

    @_binary_left_operator('%s*(%s)')        
    def __mul__(self, other):
        pass

    @_binary_left_operator('%s!=(%s)')        
    def __ne__(self, other):
        pass

    @_binary_left_operator('%s|(%s)')        
    def __or___(self, other):
        pass

    @_binary_left_operator('%s**(%s)')        
    def __pow__(self, other):
        pass

    @_binary_left_operator('%s>>(%s)')        
    def __rshift__(self, other):
        pass

    @_binary_left_operator('%s-(%s)')        
    def __sub__(self, other):
        pass

    @_binary_left_operator('%s/(%s)')        
    def __truediv__(self, other):
        pass

    @_binary_left_operator('%s^(%s)')        
    def __xor__(self, other):
        pass

    # --------------------------------

    @_binary_right_operator('(%s)+%s')
    def __radd__(self, other):
        pass

    @_binary_right_operator('(%s)&%s')
    def __rand__(self, other):
        pass

    @_binary_right_operator('(%s)/%s')
    def __rdiv__(self, other):
        pass

    @_binary_right_operator('(%s)//%s')
    def __rfloordiv__(self, other):
        pass

    @_binary_right_operator('(%s)<<%s')
    def __rlshift__(self, other):
        pass

    @_binary_right_operator('(%s)@%s')
    def __rmatmul__(self, other):
        pass

    @_binary_right_operator('(%s)%%%s')
    def __rmod__(self, other):
        pass

    @_binary_right_operator('(%s)*%s')
    def __rmul__(self, other):
        pass

    @_binary_right_operator('(%s)|%s')
    def __ror___(self, other):
        pass

    @_binary_right_operator('(%s)**%s')
    def __rpow__(self, other):
        pass

    @_binary_right_operator('(%s)>>%s')
    def __rrshift__(self, other):
        pass

    @_binary_right_operator('(%s)-%s')
    def __rsub__(self, other):
        pass

    @_binary_right_operator('(%s)/%s')
    def __rtruediv__(self, other):
        pass

    @_binary_right_operator('(%s)^%s')
    def __rxor__(self, other):
        pass

    # --------------------------------

    @_unary_operator('~(%s)')
    def __invert__(self, other):
        pass

    @_unary_operator('-(%s)')
    def __neg__(self, other):
        pass

    @_unary_operator('+(%s)')
    def __pos__(self, other):
        pass



# Make a vector
# =============

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


# Make a function with the generator expression
# =============================================

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
        self._send = self._generator.gi_frame.f_locals['.0'].send

    @helpers.cached_property
    def _expression(self):
        # Cache the send method of the internal coroutine. Before an
        # investigation I found that the first expression_list in the for
        # statement everything is stored in the same place:
        expr_obj = self(*(_MakeExpressionString(name)
            for name in self._generator.gi_code.co_varnames[1:]))

        obj = next(expr_obj)

        return obj._expression if hasattr(obj, '_expression') else self.__name__

    def __call__(self, *args):
        """Simulate a function call."""
        # send arguments to the internal coroutine
        for a in args:
            self._send(a)
        # avance the generator and return their value
        return self._generator


# Make a matrix
# =============

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
        if type(argument) is not list:
            super().__init__(argument)
        self._array = argument

    def __getitem__(self, arg):
        return self._array.__getitem__(arg)

    def __mul__(self, multiplicant):
        assert type(multiplicant) is int
        assert multiplicant > 0

        return _MatrixMaker([self._array for j in range(0, multiplicant)])



# Variables with the .__name__ property
# =====================================

def _get_outer_globals(frame, context=1):
    """Yield all global variables in the higher (calling) frames.
    """
    while frame:
        yield frame.f_globals
        frame = frame.f_back


class _NamedInstance(_MatrixMaker):
    """Make an object with the __name__ property."""
    def __init__(self, argument):
        super().__init__(argument)
        self._name = helpers.get_name()

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
            global_variables = _get_outer_globals(inspect.currentframe())
            for glob in global_variables:
                for name, value in glob.items():
                    if value is self:
                        return name
        else:
            name = self._name
            del self._name
            return name

    def __call__(self, *args):
        result = super().__call__(*args)
        return CalledObject(result, self.__name__, args)


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


class _TypeMaker(_NamedInstance):
    """A class that have all shared behaviours of all numeric types."""
