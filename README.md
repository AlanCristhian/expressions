# expressions


An experimenta library that alow you define functions with *generator
expressions*. E.g.: in the quadratic formula, the expression underneath the
square root sign is the discriminant of the quadratic equation, and is defined
as:

![Discriminant](https://github.com/AlanCristhian/expressions/blob/master/discriminant.png)

The above mathematical expression can be writed with the following notation in
Python:

```python
>>> from expressions import Real
>>> discriminant = Real(b**2 - 4*a*c for (a, b, c) in Real**3)
>>> discriminant(1, 2, 3)
-8
```