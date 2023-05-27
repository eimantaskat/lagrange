
from functions import LagrangeFunction
from algorithms import simplex

from typing import Callable, Optional


def optimize(objective_function: str, equality_constraints: list[str], inequality_constraints: list[str], x0: list[float], lambdas: Optional[list[float]] = None, tol: Optional[float] = 1e-4, alpha: Optional[float] = 0.4, r: Optional[float] = 10, tau: Optional[float] = 0.4):
	lagrange_func = LagrangeFunction(objective_function, equality_constraints, inequality_constraints)

	if lambdas is None:
		lambdas = [0.0] * (len(equality_constraints) + len(inequality_constraints))
	elif len(lambdas) != len(equality_constraints) + len(inequality_constraints):
		raise ValueError('Number of lambdas must match the number of constraints')

	while r > tol:
		x0 = simplex(lagrange_func, x0, lambdas, r, alpha)
		r *= tau
		for i, constraint in enumerate(equality_constraints + inequality_constraints):
				lambdas[i] += 1/r * lagrange_func.calculate_constraint_value(x0, constraint)

	return x0
