# Advanced SpaceTime Engineering Research software core.
# Contains mathematical and utility functions and classes
# that allow ASTER's engine to work.

# Lux Bodell, 2023.
# This code is licensed under the Creative Commons BY-NC-ND
# license. That means that you can use it and learn from it
# however you'd like, but you can't use it for commercial
# purposes or prepare derivative works of it.

from typing import Iterable
from typing import Callable
from typing import Union

Scalar = Union[int, float]

from math import sqrt

class Vector:
	def __init__(self, x: float, y: float, z: float) -> None:
		self.x, self.y, self.z = x, y, z

	def __repr__(self) -> str:
		return "<" + ", ".join(map(repr, self)) + ">"

	def __iter__(self) -> Iterable[float]:
		return iter((self.x, self.y, self.z))

	# basic vector ops

	def __add__(self, other: "Vector") -> "Vector":
		return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

	def __iadd__(self, other: "Vector") -> "Vector":
		return self + other

	def __sub__(self, other: "Vector") -> "Vector":
		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

	def __isub__(self, other: "Vector") -> "Vector":
		return self - other

	def __mul__(self, factor: float) -> "Vector":
		return Vector(self.x * factor, self.y * factor, self.z * factor)

	def __imul__(self, factor: float) -> "Vector":
		return self * factor

	def __truediv__(self, factor: float) -> "Vector":
		return Vector(self.x / factor, self.y / factor, self.z / factor)

	def __itruediv__(self, factor: float) -> "Vector":
		return self / factor

	def __abs__(self) -> float:
		return sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	# misc

	def euclidean(self, other: "Vector") -> Scalar:
		return abs(self - other)

	def normal(self):
		return self / abs(self)

class Integrator:
	def __init__(self, resolution: int=1000) -> None:
		self.resolution = resolution

	def riemannIntegral(self, f: Callable[[Scalar], Scalar], a: Scalar, b: Scalar) -> Scalar:
		dx = (b - a) / self.resolution
		s = 0
		for i in range(self.resolution):
			xi = a + i * dx
			s += f(xi)
		return s

	def fieldLineIntegral(f: Callable[[Vector], Scalar], a: Vector, b: Vector) -> Scalar:
		dX = Vector.euclidean(a, b)
		norm = (a - b).normal()
		p = lambda x: a + (norm * (x * dX))
		g = lambda x: f(p(x))

		return self.riemannIntegral(p, 0, 1)
