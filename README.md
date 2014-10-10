# expressions

An experimental library that allow your define functions that do *type
checking* with their arguments and their returned value in execution time.
Also, does all that with a **declarative syntax**.

For example, in the quadratic formula, the expression underneath the square
root sign is the discriminant of the quadratic equation, and is defined as:

![Discriminant](https://github.com/AlanCristhian/expressions/blob/master/discriminant.png)

The above mathematical expression can be writed with the following notation in
Python:

```python
discriminant = Real(b**2 - 4*a*c for (a, b, c) in Real**3)
```

The `Real` class in `expressions` module translate the *generator expression*
to the function:

```python
def function_expression(a, b, c):
    assert isinstance(a, Real)
    assert isinstance(b, Real)
    assert isinstance(b, Real)
    _Chzy0p3w4dVFL2yfahCJC6 = b**2 - 4*a*c
    assert isinstance(_Chzy0p3w4dVFL2yfahCJC6, Real)
    return _Chzy0p3w4dVFL2yfahCJC6
```

Below is the complete example written in Python:

```python
>>> from expressions import Real
>>> discriminant = Real(b**2 - 4*a*c for (a, b, c) in Real**3)
>>> discriminant(1, 2, 3)
-8
```