"""A set of utility functions."""


class cached_property:
    """ A property that is only computed once per instance and then replaces
    itself with an ordinary attribute. Deleting the attribute resets the
    property.
    """
    def __init__(self, function):
        self.__doc__ = getattr(function, '__doc__')
        self.function = function

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.function.__name__] = self.function(obj)
        return value
