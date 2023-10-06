from typing import Union
from typing import Iterable
from typing import Tuple
from typing import Any
from typing import Callable

from math import sqrt

Scalar = Union[int, float]

class Vector:

	"""
	Vector class, supporting most fundamental vector operations.
	"""

	def __init__(self, x: Scalar, y: Scalar, z: Scalar) -> None:
		self.x, self.y, self.z = x, y, z

	def __repr__(self) -> str:
		return "<" + ", ".join(map(str, self)) + ">"

	def __abs__(self) -> Scalar:
		return sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def __iter__(self) -> Iterable[Scalar]:
		return iter((self.x, self.y, self.z))

	def __eq__(self, other: "Vector") -> bool:
		return (self.x, self.y, self.z) == (other.x, other.y, other.z)

	def __neq__(self, other: "Vector") -> bool:
		return not (self == other)

	# Vector operations

	def dot(self, other: "Vector") -> Scalar:
		return sum([xn * yn for xn, yn in zip(self, other)])

	def cross(self, other: "Vector") -> "Vector":
		return Vector(
			x = (self.y * other.z) - (self.z * other.y),
			y = (self.x * other.z) - (self.z * other.x),
			z = (self.x * other.y) - (self.y * other.x)
		)

	def angle(self, other: "Vector") -> Scalar:
		return acos((Vector.dot(self, other)) / (abs(self) * abs(other)))

	def normal(self) -> "Vector":
		return self / abs(self)

	# Basic operations

	def __add__(self, other: "Vector") -> "Vector":
		return Vector(
			x = self.x + other.x,
			y = self.y + other.y,
			z = self.z + other.z
		)

	def __sub__(self, other: "Vector") -> "Vector":
		return Vector(
			x = self.x - other.x,
			y = self.y - other.y,
			z = self.z - other.z
		)

	def __mul__(self, factor: Scalar) -> "Vector":
		return Vector(
			x = self.x * factor,
			y = self.y * factor,
			z = self.z * factor
		)

	def __truediv__(self, factor: Scalar) -> "Vector":
		return Vector(
			x = self.x / factor,
			y = self.y / factor,
			z = self.z / factor
		)

	def __iadd__(self, other: "Vector") -> "Vector":
		return self + other

	def __isub__(self, other: "Vector") -> "Vector":
		return self - other

	def __imul__(self, other: Scalar) -> "Vector":
		return self * other

	def __rmul__(self, other: Scalar) -> "Vector":
		return self * other

	def __itruediv__(self, other: "Vector") -> "Vector":
		return self / other

	# Miscellaneous

	@staticmethod
	def mean(*vectors: tuple["Vector"]) -> "Vector":
		v = Vector(0, 0, 0)
		for vector in vectors:
			v += vector
		return v

	@staticmethod
	def weightedMean(vectors: Iterable["Vector"], weights: Iterable[Scalar]) -> "Vector":
		weightedSum = Vector(0, 0, 0)
		totalWeight = sum(weights)

		for vector, weight in zip(vectors, weights):
			weightedSum += vector * weight

		return weightedSum / totalWeight
	
	@classmethod
	def zero(cls) -> "Vector":
		return cls(0, 0, 0)
	
class Calculus:

	def __init__(self, h: Scalar=0.000001) -> None:
		self.h = h

	def gradient(self, f: Callable[[Vector], Scalar], v: Vector) -> Vector:
		i = f(v)
		gx = (i - f(v + Vector(self.h, 0, 0))).x / self.h
		gy = (i - f(v + Vector(0, self.h, 0))).y / self.h
		gz = (i - f(v + Vector(0, 0, self.h))).z / self.h
		return Vector(gx, gy, gz)

	def divergence(self, f: Callable[[Vector], Scalar], v: Vector) -> Vector:
		g = self.gradient(f, v)
		return g.x + g.y + g.z
	
	