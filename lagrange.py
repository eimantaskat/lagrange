
from __future__ import annotations
from functools import reduce
from typing import Union, Optional, Sequence, Iterable
import collections.abc
import itertools


def help():
	print("""+---------------------------------------------------------------------------------------
| Determine the value at the origin of the domain (*e.g.*, where *x* = 0)
| given a collection of points. The point information can be represented as
| a collection of two-component coordinates, as a dictionary, or as a sequence
| of values.
| 
| :param points: Collection of points to interpolate.
| :param modulus: Modulus representing the finite field within which to interpolate.
| :param degree: Degree of the target polynomial.
| 
| >>> from lagrange import interpolate
| >>>
| >>> interpolate({(1, 15), (2, 9), (3, 3)}, 17)
| >>> 4
| >>> interpolate({1: 4, 2: 6, 3: 8, 4: 10, 5: 12}, modulus=65537)
| >>> 2
| >>> 
| >>> interpolate({1: 4, 2: 6, 3: 8, 4: 10, 5: 12}, degree=4, modulus=65537)
| >>> 2
| >>> 
| >>> interpolate({1: 4, 2: 6, 3: 8, 4: 10, 5: 12}, degree=1, modulus=65537)
| >>> 2
| >>> 
| >>> interpolate({49: 200, 5: 24, 3: 16}, degree=2, modulus=65537)
| >>> 4
| >>> 
| >>> interpolate({49: 200, 5: 24, 3: 16}, degree=1, modulus=65537)
| >>> 4
| >>> 
| >>> interpolate({1: 16, 2: 25, 3: 36}, degree=1, modulus=65537)
| >>> 7
| >>> 
| >>> interpolate({3: 36, 1: 16, 2: 25}, degree=1, modulus=65537)
| >>> 6
| >>> 
| >>> interpolate({1: 16, 2: 25, 3: 36}, degree=2, modulus=65537)
| >>> 9
| >>> 
| >>> interpolate({3: 36, 1: 16, 2: 25}, degree=2, modulus=65537)
| >>> 9
| >>> 
| >>> interpolate({5: 64, 2: 25, 3: 36}, degree=2, modulus=65537)
| >>> 9
+---------------------------------------------------------------------------------------""")


def interpolate(points: Union[dict, Sequence[int], Iterable[Sequence[int]]], modulus: int, degree: Optional[int] = None) -> int:
	values = None # Initially, assume that the supplied point data is not valid.

	if isinstance(points, dict):
		if not (all(isinstance(k, int) for k in points.keys()) and all(isinstance(v, int) for v in points.values())):
			raise TypeError(
				'dictionary that represents points must have integer keys and values')
		values = points # Valid representation.

	elif isinstance(points, collections.abc.Iterable):
		is_sequence = isinstance(points, collections.abc.Sequence) # If iterable contains integers.
		entries = list(points)

		if all(isinstance(e, int) for e in entries):
			if not is_sequence:
				raise TypeError('iterable of integers that represents points must be a sequence')
			values = dict(zip(range(1, len(entries) + 1), entries)) # Valid representation.

		elif all(isinstance(e, collections.abc.Sequence) for e in entries):
			entries = [tuple(e) for e in entries]
			if not all(len(e) == 2 and all(isinstance(c, int) for c in e) for e in entries):
				raise TypeError(
					'iterable that represents points must contain integers ' + \
					'or two-element sequences of integers')
			values = dict(entries) # Valid representation.

	if values is None: raise TypeError('expecting dictionary or iterable that represents points')
	if len(values) == 0: raise ValueError('at least one point is required')
	if not isinstance(modulus, int): raise TypeError('expecting an integer prime modulus')
	if modulus <= 1: raise ValueError('expecting a positive integer prime modulus')

	if degree is not None:
		if not isinstance(degree, int): raise TypeError('expecting an integer degree')
		if degree < 0: raise ValueError('expecting a nonnegative integer degree')

	degree = degree or len(points) - 1
	if len(values) <= degree:
		raise ValueError('not enough points for a unique interpolation')

	# Restrict the set of points used in the interpolation.
	xs = list(values.keys())[:degree + 1]

	def _inverse(a: int, prime: int) -> int:
		return pow(a, prime - 2, prime)

	# Field arithmetic helper functions.
	mul = lambda a, b: (a % modulus) * b % modulus
	div = lambda a, b: mul(a, _inverse(b, modulus))

	# Compute the value of each unique Lagrange basis polynomial at ``0``,
	# then sum them all up to get the resulting value at ``0``.
	return sum(
		reduce(mul, itertools.chain([values[x]], (
			div(0 - x_known, x - x_known) for x_known in xs if x_known is not x
			)), 1) for x in xs) % modulus
