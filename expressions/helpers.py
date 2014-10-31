"""A set of utility functions."""

import traceback


def set_name():
    """Find the name of the instance of the current class.
    Then store it in the .__name__ attribute."""
    *_, text = traceback.extract_stack()[-3]
    name, *_ = text.split('=')
    return name.strip()
