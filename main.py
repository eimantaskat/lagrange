import numpy as np
import sympy as sp
from optimizations_algorithms import simplex
from function_wrapper import FunctionWrapper


class LagrangeFunction:
	def __init__(self, objective_function: str, equality_constraints: list, inequality_constraints: list):
		symbolic_variables = sp.symbols('x y z')
		self.objective_function = FunctionWrapper(function=objective_function, symbols=symbolic_variables)

		self.constraint_functions = {}

		for constraint in equality_constraints:
			self.constraint_functions[constraint] = sp.lambdify(symbolic_variables, sp.sympify(constraint), 'numpy')

		for constraint in inequality_constraints:
			self.constraint_functions[constraint] = sp.lambdify(symbolic_variables, sp.Max(sp.sympify(constraint), 0), 'numpy')


	def __call__(self, X, lambdas, r):
		objective_value = self.objective_function(X)
		constraints_values = [constraint(*X) for constraint in self.constraint_functions.values()]

		lagrange_value = objective_value + sum([lam * constraint_value for lam, constraint_value in zip(lambdas, constraints_values)]) + (1 / r) * sum([constraint_value**2 for constraint_value in constraints_values])
		return lagrange_value


	def calculate_constraint_value(self, X, constraint):
		return self.constraint_functions[constraint](*X)


if __name__ == '__main__':
	tol = 1e-4
	alpha = 0.4

	objective_function = '-x*y*z'
	equality_constraints = ['2*x*y + 2*x*z + 2*y*z - 1']
	inequality_constraints = ['-x', '-y', '-z']

	lagrange_func = LagrangeFunction(objective_function, equality_constraints, inequality_constraints)

	# Initial values
	initial_values = np.array([[0, 0, 0], [1, 1, 1], [.5, .2, .0]])
	for x0 in initial_values:
		print(f'Initial values: {x0}')
		iterations = 0
		lambdas = [0.0] * (len(equality_constraints) + len(inequality_constraints))
		r = 10

		while r > tol:
			# Use an optimization algorithm to minimize the Lagrange function
			x0, iter_count = simplex(lagrange_func, x0, lambdas, r, alpha)
			iterations += iter_count
			r = 0.4 * r  # update the penalty parameter
			for i, constraint in enumerate(equality_constraints + inequality_constraints):
				lambdas[i] += 1/r * lagrange_func.calculate_constraint_value(x0, constraint)

		print(f'Iterations: {iterations}')
		print(f'Objective function call count: {lagrange_func.objective_function.times_called}')
		print(f'Optimal values: {x0}')
		print(f'Objective function value: {lagrange_func.objective_function(x0)}')
		print(f'Constraint values: {[lagrange_func.calculate_constraint_value(x0, constraint) for constraint in equality_constraints + inequality_constraints]}')
		print(f'Lambda values: {lambdas}')
		print(f'Penalty parameter: {r}')
		print()
