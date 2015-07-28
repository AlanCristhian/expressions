# symbolic

An experimental library that let your define mathematical expressions.

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

### Domain of a function (not yet implemented)

You can define the domain of a function. E.g: `D` is cilinder with
`height = 2` and `radius = 1` and is paralell to `z` axis:

`D = {(x, y, z) ∀ (x, y, z) ∊ ℝ³ | 0 ≤ x ≤ 2, 0 ≤ y² + z² ≤ 1}`

Is translated to Python3 as:

```python
D = Domain([0 <= x <= 2, 0 <= y**2 + z**2 <= 1] for (x, y, z) in Real**3)
```

### Range of a function (not yet implemented)

Also you can define the range of a function. E.g:

`R = {(x, y, z) ∀ (x, y, z) ∊ ℝ³ | 0 ≤ x ≤ 2, 0 < y < 2, 2 > z > -2 }`

Is translated to Python3 as:

```python
R = Range([0 <= x <= 2, 0 < y <= 2, 2 > z > -2] for (x, y, z) in Real**3)
```

### Precondition and postcondition in a function (not yet implemented)

Supose that you want to validate the input and output of a function. You
can use the domain and range to do that.

```python
my_domain = Domain([-1 < x < 1, -1 < y < 1] for (x, y) in Real**2)
my_range = Range([-2 < z < 2] for z in Real)
function = my_range(x + y for (x, y) in my_domain)
```

The `function` object check that the argument meet the condition described
in `my_domain` and theck that their result is between -2 and 2.

## System of equalities

```python
>>> from symbolic import System, Real
>>> system = System([
...      -x1 +  2*x2 -  3*x3 ==  4,
...     5*x1 -  6*x2 +  7*x3 == -8,
...     9*x1 + 10*x2 - 11*x3 == 12]
...         for (x1, x2, x3) in Real**3)
>>> system.solve()
[1 == 0.0, x2 == -1.0, x3 == -2.0]
```

## System of inequalities

```python
>>> from symbolic import System, Real
>>> system = System(2 - 3*x < 7 for x in in Real)
>>> system.solve()
[x > 1.666667]
```
