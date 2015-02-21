def _get_shape(list_of_lists):
    """Get the dimension of the matrix."""
    shape = ()
    item = list_of_lists[0]
    if type(item) is list:
        shape += _get_shape(item)
    else:
        shape += (len(list_of_lists),)
    return shape


class Matrix(dict):
    def __init__(self, iterable=None):
        if iterable is not None:
            n = len(iterable)
            for item in iterable:
                pass

    def __getitem__(self, key):
        pass
