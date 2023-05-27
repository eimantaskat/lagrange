
from functions import LagrangeFunction
from algorithms import simplex

import numpy as np


if __name__ == '__main__':
	tol = 1e-4
	alpha = 0.4
	tau = 0.4

	objective_function = '-x*y*z'
	equality_constraints = ['2*x*y + 2*x*z + 2*y*z - 1']
	inequality_constraints = ['-x', '-y', '-z']

	lagrange_func = LagrangeFunction(objective_function, equality_constraints, inequality_constraints)

	# Initial values
	initial_values = np.array([[0, 0, 0], [1, 1, 1], [.5, .2, .0]])
	for x0 in initial_values:
		lagrange_func.objective_function.clear_cache()
		print(f'Initial values: {x0}')
		iterations = 0
		lambdas = [0.0] * (len(equality_constraints) + len(inequality_constraints))
		r = 10

		while r > tol:
			# Use an optimization algorithm to minimize the Lagrange function
			x0, iter_count = simplex(lagrange_func, x0, lambdas, r, alpha, count_iterations=True)
			iterations += iter_count
			r = tau * r  # update the penalty parameter
			for i, constraint in enumerate(equality_constraints + inequality_constraints):
				lambdas[i] += 1/r * lagrange_func.calculate_constraint_value(x0, constraint) # update the Lagrange multipliers

		print(f'Iterations: {iterations}')
		print(f'Objective function call count: {lagrange_func.objective_function.times_called}')
		print(f'Optimal point: {x0}')
		print(f'Objective function value: {lagrange_func.objective_function(x0)}')
		print(f'Constraint values: {[lagrange_func.calculate_constraint_value(x0, constraint) for constraint in equality_constraints + inequality_constraints]}')
		print(f'Lambda values: {lambdas}')
		print(f'Penalty parameter: {r}')
		print()
