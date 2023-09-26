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

from struct import pack

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

	def dot(self, other: "Vector") -> Scalar:
		return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

	def cross(self, other: "Vector") -> "Vector":
		return Vector(
			(self.y * other.z) - (self.z * other.y),
			(self.x * other.z) - (self.z * other.x),
			(self.x * other.y) - (self.y * other.x)
		)

	# misc

	def euclidean(self, other: "Vector") -> Scalar:
		return abs(self - other)

	def normal(self):
		return self / abs(self)

	def __bytes__(self) -> bytes:
		return pack("!ddd", self.x, self.y, self.z)

	@classmethod
	def fromBytes(cls, data: bytes):
		x, y, z = unpack("!ddd", data)
		return cls(x, y, z)

class Integrator:
	# Class to generate monovariate and trivariate Riemann integrals

	def __init__(self, resolution: int=1000) -> None:
		self.resolution = resolution

	def monovariate(self, f: Callable[[Scalar], Scalar], a: Scalar, b: Scalar) -> Scalar:
		dx = (b - a) / self.resolution
		s = 0
		for i in range(self.resolution):
			xi = a + i * dx
			s += f(xi) / self.resolution
		return s

	def trivariate(self, f: Callable[[Vector], Scalar], a: Vector, b: Vector) -> Scalar:
		stepX = (b.x - a.x) / self.resolution
		stepY = (b.y - a.y) / self.resolution
		stepZ = (b.z - a.z) / self.resolution
		step = abs(Vector(stepX, stepY, stepZ))

		s = 0
		for i in range(self.resolution):
			x = a.x + (stepX * i)
			y = a.y + (stepY * i)
			z = a.z + (stepZ * i)
			v = Vector(x, y, z)
			s += f(v) * step

		return s
