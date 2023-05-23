
## How to use it?
To enter the python console:
```console
> cd <root of the project>
> python3
```

When entered the python3 console:
```console
>>> from lagrange import interpolate, help
>>> help()
>>> interpolate({(1, 15), (2, 9), (3, 3)}, 17)  # Should return 4
```

## API
```python
Determine the value at the origin of the domain (*e.g.*, where *x* = 0)
given a collection of points. The point information can be represented as
a collection of two-component coordinates, as a dictionary, or as a sequence
of values.

:param points: Collection of points to interpolate.
:param modulus: Modulus representing the finite field within which to interpolate.
:param degree: Degree of the target polynomial.

>>> from lagrange import interpolate, help
>>> 
>>> help()
>>> 
>>> interpolate({(1, 15), (2, 9), (3, 3)}, 17)
>>> 4
>>> interpolate({1: 4, 2: 6, 3: 8, 4: 10, 5: 12}, modulus=65537)
>>> 2
>>> 
>>> interpolate({1: 4, 2: 6, 3: 8, 4: 10, 5: 12}, degree=4, modulus=65537)
>>> 2
>>> 
>>> interpolate({1: 4, 2: 6, 3: 8, 4: 10, 5: 12}, degree=1, modulus=65537)
>>> 2
>>> 
>>> interpolate({49: 200, 5: 24, 3: 16}, degree=2, modulus=65537)
>>> 4
>>> 
>>> interpolate({49: 200, 5: 24, 3: 16}, degree=1, modulus=65537)
>>> 4
>>> 
>>> interpolate({1: 16, 2: 25, 3: 36}, degree=1, modulus=65537)
>>> 7
>>> 
>>> interpolate({3: 36, 1: 16, 2: 25}, degree=1, modulus=65537)
>>> 6
>>> 
>>> interpolate({1: 16, 2: 25, 3: 36}, degree=2, modulus=65537)
>>> 9
>>> 
>>> interpolate({3: 36, 1: 16, 2: 25}, degree=2, modulus=65537)
>>> 9
>>> 
>>> interpolate({5: 64, 2: 25, 3: 36}, degree=2, modulus=65537)
>>> 9
```