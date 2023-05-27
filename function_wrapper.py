import numpy as np
import sympy as sp


class Function(dict):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		function = kwargs.get('f', None)
		symbols = kwargs.get('symbols', None)

		self._function = sp.lambdify(symbols, sp.sympify(function), 'numpy')

		self.clear()


	def __missing__(self, key: np.ndarray) -> float:
		value = self._function(*key)
		self[key] = value
		return value


class FunctionWrapper():
	def __init__(self, **kwargs) -> None:
		function = kwargs.get('function', None)
		symbols = kwargs.get('symbols', None)

		self._symbols = symbols
		self._function = Function(f=function, symbols=symbols)


	@property
	def times_called(self) -> int:
		return len(self._function.keys())


	def __call__(self, X) -> float:
		return self._function[*X]


	def clear_cache(self) -> None:
		self._function.clear()
