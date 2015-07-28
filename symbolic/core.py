"""
A library with base classes and metaclasses that let me
define numeric sets and some mathematical expressions.
"""


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


_LEFT_OPERATOR = {
    '__add__': '%s+(%s)',
    '__and__': '%s&(%s)',
    '__div__': '%s/(%s)',
    '__eq__': '%s==(%s)',
    '__floordiv__': '%s//(%s)',
    '__ge__': '%s>=(%s)',
    '__gt__': '%s>(%s)',
    '__le__': '%s<=(%s)',
    '__lshift__': '%s<<(%s)',
    '__lt__': '%s<(%s)',
    '__matmul__': '%s@(%s)',
    '__mod__': '%s%%(%s)',
    '__mul__': '%s*(%s)',
    '__ne__': '%s!=(%s)',
    '__or__': '%s|(%s)',
    '__pow__': '%s**(%s)',
    '__rshift__': '%s>>(%s)',
    '__sub__': '%s-(%s)',
    '__truediv__': '%s/(%s)',
    '__xor__': '%s^(%s)',
}


_RIGHT_OPERATOR = {
    '__radd__': '(%s)+%s',
    '__rand__': '(%s)&%s',
    '__rdiv__': '(%s)/%s',
    '__rfloordiv__': '(%s)//%s',
    '__rlshift__': '(%s)<<%s',
    '__rmatmul__': '(%s)@%s',
    '__rmod__': '(%s)%%%s',
    '__rmul__': '(%s)*%s',
    '__ror__': '(%s)|%s',
    '__rpow__': '(%s)**%s',
    '__rrshift__': '(%s)>>%s',
    '__rsub__': '(%s)-%s',
    '__rtruediv__': '(%s)/%s',
    '__rxor__': '(%s)^%s',
}


_UNARY_OPERATOR = {
    '__invert__': '~(%s)',
    '__neg__': '-(%s)',
    '__pos__': '+(%s)',
}


_BUILT_IN_FUNCTIONS = {
    '__abs__': 'abs(%s%s%s)',
    '__round__': 'round(%s%s%s)',
    '__reversed__': 'reversed(%s%s%s)',

    # FIXME: folowing methods did not work. View FailedExpressionBehaviours
    # class in the tests/test_suger.py module.

    # '__len__': 'len(%s%s%s)',
    # '__instancecheck__': 'isinstance(%s%s%s)',
    # '__subclasscheck__': 'issubclass(%s%s%s)',
    # '__contains__': 'contains(%s%s%s)',
    # '__iter__': 'iter(%s%s%s)',

    # TODO:
    # '__bytes__': 'bytes(%s%s%s)',
    # '__format__': 'format(%s%s%s)',
    # '__hash__': 'hash(%s%s%s)',
    # '__bool__': 'bool(%s%s%s)',
    # '__setattr__': 'setattr(%s%s%s)',
    # '__delattr__': 'delattr(%s%s%s)',
    # '__dir__': 'dir(%s%s%s)',
}


def _left_operator(template):
    """Return a function that make an expression
    string with a binary left operator.
    """
    def operator(self, other):
        result = Expression("")
        if hasattr(other, '__expr__'):
            result.__expr__ = template % (self.__expr__, other.__expr__)
        else:
            result.__expr__ = template % (self.__expr__, repr(other))
        return result
    return operator


def _right_operator(template):
    """Return a function that make an expression string with
    an binary operator placed at the right of the variable.
    """
    def operator(self, other):
        result = Expression("")
        if hasattr(other, '__expr__'):
            result.__expr__ = template % (other.__expr__, self.__expr__)
        else:
            result.__expr__ = template % (repr(other), self.__expr__)
        return result
    return operator


def _unary_operator(template):
    """Return a function that make an
    expression string with an unary operator.
    """
    def operator(self):
        result = Expression("")
        result.__expr__ = template % self.__expr__
        return result
    return operator


# The __call__ method difer of the other special methods in the serparator
# variable. So, I add such variable as default argument.
def _built_in_function(template, separator=', '):
    """Return a function that make an
    expression with an built in function.
    """
    def function(self, *args, **kwds):
        formated_kwds, formated_args = "", ""
        if args != ():
            formated_args = separator + repr(args)[1:][:-2]
        if kwds != {}:
            add_equal = ('%s=%r' % (key, value) for key, value in kwds.items())
            formated_kwds = ', ' + ', '.join(add_equal)
        result = Expression("")
        result.__expr__ = template % (self.__expr__, formated_args,
                                      formated_kwds)
        return result
    return function


class _Operators(type):
    """All operators of the new class will
    return an instance of the Expression class.
    """
    def __new__(cls, name, bases, namespace):
        namespace.update({function: _left_operator(template) for
                          function, template in _LEFT_OPERATOR.items()})
        namespace.update({function: _right_operator(template) for
                          function, template in _RIGHT_OPERATOR.items()})
        namespace.update({function: _unary_operator(template) for
                          function, template in _UNARY_OPERATOR.items()})
        namespace.update({function: _built_in_function(template) for
                          function, template in _BUILT_IN_FUNCTIONS.items()})
        call_method = _built_in_function(template='%s(%s%s)', separator="")
        namespace.update({'__call__': call_method})
        new_class = super().__new__(cls, name, bases, namespace)
        return new_class


class Expression(metaclass=_Operators):
    """Create an object that store all
    math operations in which it is involved.
    """
    def __init__(self, name, bases=()):
        self.__expr__ = name

    def __repr__(self):
        return self.__expr__

    def __getitem__(self, attr):
        result = Expression("")
        result.__expr__ = '(%s)[%r]' % (self.__expr__, attr)
        return result

    def __hash__(self):
        return hash(self.__expr__)


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


class CalledObject(Expression):
    """This object is created when you call the the function."""
    def __init__(self, generator, name, args):
        self._generator = generator
        self.__expr__ = name + repr(args).replace(',)', ')')

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
        return self.__expr__


# Third, I use the coroutine-object returned by the __iter__() method to pass
# values in each iteration of the generator expression. Such values act like
# funtions parameters. The generator-expression is an consumer.

class CallableObject(NamedObject):
    def __init__(self, generator):
        super().__init__()
        self._generator = generator
        self._send = self._generator.gi_frame.f_locals['.0'].send
        self._var_names = self._generator.gi_code.co_varnames[1:]

    def _make_expression(self):
        """Send an Expression() object to the generator. Then
        return the object with the ".__expr__" property."""
        # CAVEAT: everything the first var name in gi_code.co_varnames is "0.0"
        # This is the name of the iterator used in the first *for* statement
        # in the generator.
        expr_obj = self(*(Expression(name) for name in self._var_names))
        return next(expr_obj)

    @utils.cached_property
    def __expr__(self):
        obj = self._make_expression()
        return obj.__expr__ if hasattr(obj, '__expr__') \
        else self.__name__

    def __call__(self, *args):
        """Simulate a function call."""
        # send arguments to the internal coroutine
        self._send(args[0]) if len(args) is 1 else self._send(args)

        # avance the generator and return their value
        return CalledObject(self._generator, self.__name__, args)

    def eval(self, *args):
        return next(self(*args))


"""
Make a matrix
=============

Now, supose that I wish to define a matrix with the sintax:

>>> A = Real**3*4

The `A` object is a matrix with 3 rows and 4 columns. The
`MatrixType.__mul__()` method set such feature to the object created
with the `Real**3` expression.
"""

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

class BaseRelation:
    def __init__(self, left, right):
        if isinstance(left, (int, float, complex)) and isinstance(right, str):
            self.left = right
            self.right = left
        else:
            self.left = left
            self.right = right

    def __eq__(self, other):
        return (type(self) is type(other) and
                self.left == other.left and
                self.right == other.right)


class EqMeta(type):
    def __new__(cls, name, bases, namespace):
        namespace.update({key: value
                         for key, value in EqMeta.__dict__.items()
                             if key != "__new__"
                             if key != "__doc__"
                             if key != "__repr__"
                             if key != "__module__"})
        return super().__new__(cls, name, bases, namespace)

    def __repr__(cls): return "=="

    def __pos__(self): return self

    def __neg__(self): return self

    def __add__(self, other): return self

    def __radd__(self, other): return self

    def __sub__(self, other): return self

    def __rsub__(self, other): return self

    def __truediv__(self, other): return self

    def __rtruediv__(self, other): return self

    def __mul__(self, other): return self

    def __rmul__(self, other): return self


class Eq(BaseRelation, metaclass=EqMeta):
    def __repr__(self):
        return "%s == %r" % (self.left, self.right)


class NeMeta(EqMeta):
    def __repr__(self):
        return "!="


class Ne(BaseRelation, metaclass=NeMeta):
    def __repr__(self):
        return "%s != %r" % (self.left, self.right)


class LtMeta(type):
    def __new__(cls, name, bases, namespace):
        return super().__new__(cls, name, bases, namespace)

    def __repr__(self): return "<"

    def __neg__(self): return Gt

    def __rsub__(self, other): return Gt

    def __truediv__(self, other): return Gt

    def __rtruediv__(self, other): return Gt

    def __mul__(self, other): return Gt

    def __rmul__(self, other): return Gt


class Lt(BaseRelation, metaclass=LtMeta):
    def __repr__(self):
        return "%s < %r" % (self.left, self.right)

    def __neg__(self):
        return Gt(self.left, self.right)

    def __rsub__(self, other):
        return Gt(self.left, self.right)

    def __truediv__(self, other):
        return Gt(self.left, self.right)

    def __rtruediv__(self, other):
        return Gt(self.left, self.right)

    def __mul__(self, other):
        return Gt(self.left, self.right)

    def __rmul__(self, other):
        return Gt(self.left, self.right)


class GtMeta(type):
    def __new__(cls, name, bases, namespace):
        return super().__new__(cls, name, bases, namespace)

    def __repr__(self): return ">"

    def __neg__(self): return Lt

    def __rsub__(self, other): return Lt

    def __truediv__(self, other): return Lt

    def __rtruediv__(self, other): return Lt

    def __mul__(self, other): return Lt

    def __rmul__(self, other): return Lt


class Gt(BaseRelation, metaclass=GtMeta):
    def __repr__(self):
        return "%s > %r" % (self.left, self.right)

    def __neg__(self):
        return Lt(self.left, self.right)

    def __rsub__(self, other):
        return Lt(self.left, self.right)

    def __truediv__(self, other):
        return Lt(self.left, self.right)

    def __rtruediv__(self, other):
        return Lt(self.left, self.right)

    def __mul__(self, other):
        return Lt(self.left, self.right)

    def __rmul__(self, other):
        return Lt(self.left, self.right)


class LeMeta(type):
    def __new__(cls, name, bases, namespace):
        return super().__new__(cls, name, bases, namespace)

    def __repr__(self): return "<="

    def __neg__(self): return Ge

    def __rsub__(self, other): return Ge

    def __truediv__(self, other): return Ge

    def __rtruediv__(self, other): return Ge

    def __mul__(self, other): return Ge

    def __rmul__(self, other): return Ge


class Le(BaseRelation, metaclass=LeMeta):
    def __repr__(self):
        return "%s <= %r" % (self.left, self.right)

    def __neg__(self):
        return Ge(self.left, self.right)

    def __rsub__(self, other):
        return Ge(self.left, self.right)

    def __truediv__(self, other):
        return Ge(self.left, self.right)

    def __rtruediv__(self, other):
        return Ge(self.left, self.right)

    def __mul__(self, other):
        return Ge(self.left, self.right)

    def __rmul__(self, other):
        return Ge(self.left, self.right)


class GeMeta(type):
    def __new__(cls, name, bases, namespace):
        return super().__new__(cls, name, bases, namespace)

    def __repr__(self): return ">="

    def __neg__(self): return Le

    def __rsub__(self, other): return Le

    def __truediv__(self, other): return Le

    def __rtruediv__(self, other): return Le

    def __mul__(self, other): return Le

    def __rmul__(self, other): return Le


class Ge(BaseRelation, metaclass=GeMeta):
    def __repr__(self):
        return "%s >= %r" % (self.left, self.right)

    def __neg__(self):
        return Le(self.left, self.right)

    def __rsub__(self, other):
        return Le(self.left, self.right)

    def __truediv__(self, other):
        return Le(self.left, self.right)

    def __rtruediv__(self, other):
        return Le(self.left, self.right)

    def __mul__(self, other):
        return Le(self.left, self.right)

    def __rmul__(self, other):
        return Le(self.left, self.right)
