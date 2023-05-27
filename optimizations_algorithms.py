
from typing import Callable, Optional

import numpy as np


def simplex(f: Callable, x0: np.ndarray, lambdas: np.ndarray, r: float, alpha: float, tol: Optional[float] = 1e-4, count_iterations: Optional[bool] = False):
	iter_count = 0

	# create initial simplex
	n = len(x0)
	simplex = np.zeros((n+1, n))
	simplex[0] = np.array(x0)

	# Calculate delta1 and delta2
	delta1 = (np.sqrt(n + 1) + n - 1) / (n * np.sqrt(2)) * alpha
	delta2 = (np.sqrt(n + 1) - 1) / (n * np.sqrt(2)) * alpha

	# Generate initial simplex
	for i in range(1, n+1):
		simplex[i] = simplex[0].copy()
		simplex[i, i-1] += delta2
		simplex[i, np.arange(n) != i-1] += delta1

	# iterate until convergence
	while True:
		iter_count += 1

		# find worst and best points
		values = np.array([f(point, lambdas, r) for point in simplex])
		worst = np.argmax(values)
		best = np.argmin(values)

		# calculate centroid
		xc = np.mean(np.delete(simplex, worst, axis=0), axis=0)

		# reflect worst point
		xr = 2 * xc - simplex[worst]

		if f(xr, lambdas, r) <= values[worst]:
			# replace worst point with reflected point
			simplex[worst] = xr
		else:
			# contract the simplex
			xk = (simplex[worst] + xc) / 2
			if f(xk, lambdas, r) < values[worst]:
				# replace worst point with contracted point
				simplex[worst] = xk
			else:
				# shrink the simplex towards the best point
				simplex[1:] = (simplex[1:] + simplex[best]) / 2

		# check if simplex is small enough
		if np.max(np.abs(simplex - simplex[best])) < tol:
			break

	if count_iterations:
		return simplex[best], iter_count
	return simplex[best]
