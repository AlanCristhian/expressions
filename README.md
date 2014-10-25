# expressions

An experimental library that allow your define sympy expressions with
 **declarative syntax**.

## Matrix definition

You can define vectors and matrix whit an natural sintax:

```python
>>> from expressions.types import Real
>>> v = Real**3
>>> v
Real([0, 0, 0])
>>> u = Real([1, 2, 3])
>>> u
Real([1, 2, 3])
>>> u[1]
2
>>> u[1] = 555
>>> u
Real([1, 555, 3])
```

Also you can define matrix:

```python
>>> from expressions.types import Real
>>> A = Real**3*3
>>> A
Real([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
>>> I = Real([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
>>> I[2][1]
0
```

# Functions

For example, in the quadratic formula, the expression underneath the square
root sign is the discriminant of the quadratic equation, and is defined as:

`Δ = {b² - 4ac | (a, b, c) ∊ ℝ³}`

The above mathematical expression can be writed with the following notation in
Python:

```python
discriminant = Real(b**2 - 4*a*c Real for (a, b, c) in Real**3)
```

The `Real` class in `expressions` module translate the *generator expression*
to the function:

```python
def function_expression():
    a, b, c = sympy.Symbol('a b c', real=True)
    return b**2 - 4*a*c
delta = function_expression()
```

Below is the complete example written in Python:

```python
>>> from expressions import Real
>>> delta = Real((b**2 - 4*a*c) for (a, b, c) in Real**3)
>>> delta.subs([(a, 1), (b, 2), (c, 3)])
-8
```

#### Domain of a function

The you can define the domain of a function. E.g: `D` is cilinder with
`height = 2` and `radius = 1` and is paralell to `z` axis:

`D = {(x, y, z) | (x, y, z) ∊ ℝ³, 0 ≤ x ≤ 2, 0 ≤ y² + z² ≤ 1}`

Is translated to Python3 as:

```python
D = Real**3((x, y, z) for (x, y, z) in Real**3 if 0 <= x <= 2 if 0 <= y**2 + z**2 <= 1)
```


#### Matrix

Supose that you wish a 3x3 matrix with reals components:

```python
A = Real**3*3
```


The I matrix of 3x3 components:

```python
I = Real**3*3([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
```

The indicator function Is

```python
S = Natural([0, 1])
Is = S(
    0 if x not in S else
    1 if x in S
    for x in Natural
)
```