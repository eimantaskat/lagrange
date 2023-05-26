import numpy as np
import sympy as sp
from optimizations_algorithms import simplex

class LagrangeFunction:
	def __init__(self, objective_function: str, equality_constraints: list, inequality_constraints: list):
		self.objective_function = sp.sympify(objective_function)

		self.constraints_function = 0
		for constraint in equality_constraints:
			self.constraints_function += sp.sympify(constraint)
		for constraint in inequality_constraints:
			self.constraints_function += sp.Max(sp.sympify(constraint), 0)

		self.objective_func_lambda = sp.lambdify(('x', 'y', 'z'), self.objective_function, 'numpy')
		self.constraints_func_lambda = sp.lambdify(('x', 'y', 'z'), self.constraints_function, 'numpy')

	def __call__(self, X, lambdas, r):
		objective_value = self.objective_func_lambda(*X)
		constraints_value = self.constraints_func_lambda(*X)

		lagrange_value = objective_value + lambdas * constraints_value + (1 / r) * constraints_value**2
		return lagrange_value

	def constraint_function(self, X):
		return self.constraints_func_lambda(*X)


objective_function = '-x*y*z'
equality_constraints = ['2*x*y + 2*x*z + 2*y*z - 1']
inequality_constraints = ['-x', '-y', '-z']

lagrange_func = LagrangeFunction(objective_function, equality_constraints, inequality_constraints)

# Initial values
x0 = np.array([1, 1, 1])  # initial guess for variables
lambda_0 = 0.0  # initial guess for Lagrange multiplier
r = 10  # penalty parameter

tol = 1e-4
alpha = 0.4
while r > tol:
	# Use an optimization algorithm to minimize the Lagrange function
	x0 = simplex(lagrange_func, x0, lambda_0, r, alpha)
	r = 0.4 * r  # update the penalty parameter
	lambda_0 = lambda_0 + 1/r * lagrange_func.constraint_function(x0)  # update the Lagrange multiplier

print(x0)
