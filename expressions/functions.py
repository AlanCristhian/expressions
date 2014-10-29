"""A library that implement a new way to define functions that do
type checking."""


# I want to define a function that do type checking of arguments and values
# returned. All those with generator-expressions. E.g:

# >>> double = Integer(2*x for x in Integer)
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
    def __init__(cls, name, bases, namespace):
        return super().__init__(name, bases, namespace)

    def __iter__(cls):
        # !!!: the iter method return the _argument_sender() coroutine-object
        sender = _argument_sender()
        next(sender)
        return sender


# Third, I use the coroutine-object returned by the __iter__() method to pass
# values in each iteration of the generator expression. Such values act like
# funtions parameters. The generator-expression is an consumer.

class _MakeCallable(metaclass=_IterableMeta):
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
