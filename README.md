# symbolic

An experimental library that allow your define mathematical expressions.

## Matrix definition

You can define vectors and matrix whit an natural sintax:

```python
>>> from symbolic import Real
>>> v = Real**3
>>> v
v ∊ Real**3
>>> u = Real([1, 2, 3])
>>> u
Real([1, 2, 3])
>>> u[1]
2
>>> u[1] = 555
>>> u
Real([1, 555, 3])
```

Below is the sintax to define a matrix:

```python
>>> from symbolic import Real
>>> A = Real**3*3
>>> A
A ∊ Real**3*3
>>> I = Real([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
>>> I[2][1]
0
```

## Functions

For example, in the quadratic formula, the expression underneath the square
root sign is the discriminant of the quadratic equation, and is defined as:

`Δ: D ⊂ ℝ³ → ℝ and Δ(a, b, c) = b² - 4ac`

The above mathematical expression can be writed with the following notation in
Python:

```python
discriminant = Real(b**2 - 4*a*c for (a, b, c) in Real**3)
```

Below is the complete example written in Python:

```python
>>> from symbolic import Real
>>> delta = Real(b**2 - 4*a*c for (a, b, c) in Real**3)
>>> delta(1, 2, 3)
delta(1, 2, 3)
>>> next(delta(1, 2, 3))
-8
```

Also you can do early evaluation with the `.eval()` method:

```python
>>> from symbolic import Real
>>> delta = Real(b**2 - 4*a*c for (a, b, c) in Real**3)
>>> delta.eval(1, 2, 3)
-8
```


## System of equalities

```python
>>> from symbolic import System, Real
>>> system = System([
...      -x1 +  2*x2 -  3*x3 ==  4,
...     5*x1 -  6*x2 +  7*x3 == -8,
...     9*x1 + 10*x2 - 11*x3 == 12]
...         for (x1, x2, x3) in Real**3)
>>> system.solve()
(BinaryRelation(x1 == 0.0), BinaryRelation(x2 == -1.0), BinaryRelation(x3 == -2.0))
```

## Domain of a function (not yet implemented)

The you can define the domain of a function. E.g: `D` is cilinder with
`height = 2` and `radius = 1` and is paralell to `z` axis:

`D = {(x, y, z) ∀ (x, y, z) ∊ ℝ³ | 0 ≤ x ≤ 2, 0 ≤ y² + z² ≤ 1}`

Is translated to Python3 as:

```python
D = Domain((x, y, z) for (x, y, z) in Real**3 if 0 <= x <= 2 if 0 <= y**2 + z**2 <= 1)
```
