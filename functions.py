
import numpy as np
import sympy as sp


class Function(dict):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		function = kwargs.get('function', None)
		symbols = kwargs.get('symbols', None)

		self._function = sp.lambdify(symbols, sp.sympify(function), 'numpy')

		self.clear()


	def __missing__(self, key: np.ndarray) -> float:
		value = self._function(*key)
		self[key] = value
		return value


	@property
	def times_called(self) -> int:
		return len(self.keys())


	def __call__(self, X) -> float:
		return self[*X]


	def clear_cache(self) -> None:
		self.clear()


class LagrangeFunction:
	def __init__(self, objective_function: str, equality_constraints: list, inequality_constraints: list):
		symbolic_variables = sp.symbols('x y z')
		self.objective_function = Function(function=objective_function, symbols=symbolic_variables)

		self.constraint_functions = {}

		for constraint in equality_constraints:
			self.constraint_functions[constraint] = sp.lambdify(symbolic_variables, sp.sympify(constraint), 'numpy')

		for constraint in inequality_constraints:
			self.constraint_functions[constraint] = sp.lambdify(symbolic_variables, sp.Max(sp.sympify(constraint), 0), 'numpy')


	def __call__(self, X: np.ndarray, lambdas: np.ndarray, r: float) -> float:
		objective_value = self.objective_function(X)
		constraints_values = [constraint(*X) for constraint in self.constraint_functions.values()]

		lagrange_value = objective_value + sum([lam * constraint_value for lam, constraint_value in zip(lambdas, constraints_values)]) + (1 / r) * sum([constraint_value**2 for constraint_value in constraints_values])
		return lagrange_value


	def calculate_constraint_value(self, X: np.ndarray, constraint: str) -> float:
		return self.constraint_functions[constraint](*X)
