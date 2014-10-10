# expressions


An experimenta library that alow you define functions with *generator
expressions*. E.g.: in the quadratic formula, the expression underneath the
square root sign is the discriminant of the quadratic equation, and is defined
as:

![Discriminant](http://www.sciweavers.org/tex2img.php?eq=%20\Delta%20%28a%2C%20b%2C%20c%29%20%3A%20\Re%20^{3}%20%20\rightarrow%20\Re%20%3D%20b^{2}%20-%204ac&bc=White&fc=Black&im=jpg&fs=18&ff=mathptmx&edit=0%22%20align=%22center%22%20border=%220%22%20alt=%22%20\Delta%20%28a,%20b,%20c%29%20:%20\Re%20^{3}%20%20\rightarrow%20\Re%20=%20b^{2}%20-%204ac)

The above mathematical expression can be writed with the following notation in
Python:

```python
>>> from expressions import Real
>>> discriminant = Real(b**2 - 4*a*c for (a, b, c) in Real**3)
>>> discriminant(1, 2, 3)
-8
```