from tkinter import Tk
from tkinter import Frame
from tkinter import Label
from tkinter import Canvas
from tkinter import Entry
from tkinter import Button

from math import sqrt
from math import acos

from functools import cache

from typing import Callable
from typing import Iterable
from typing import Any
from typing import Union

# ===== Core components ===== #

Scalar = Union[int, float]

class Vector:

	"""
	Vector class, supporting most fundamental vector operations.
	"""

	def __init__(self, x: Scalar, y: Scalar, z: Scalar) -> None:
		self.x, self.y, self.z = x, y, z

	def __abs__(self) -> Scalar:
		return sqrt((x ** 2) + (y ** 2) + (z ** 2))

	def __iter__(self) -> Iterable[Scalar]:
		return iter((self.x, self.y, self.z))

	def __eq__(self, other: "Vector") -> bool:
		return (self.x, self.y, self.z) == (other.x, other.y, other.z)

	def __neq__(self, other: "Vector") -> bool:
		return not (self == other)

	# Vector operations

	def dot(self, other: "Vector") -> Scalar:
		return sum([xn * yn for xn, yn in zip(self, other])

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

	def __imul__(self, other: "Vector") -> "Vector":
		return self * other

	def __itruediv__(self, other: "Vector") -> "Vector":
		return self / other

class Calculus:

	# Differentiation methods

	CENTRAL = "central"
	FORWARD = "forward"
	BACKWARD = "backward"

	# Integration methods

	TRAPEZOIDAL = "trapezoidal"
	SIMPSON = "simpson"

	def __init__(self, resolution: int)
		self._differentiationMethod: Callable = None
		self._integrationMethod: Callable = None

		self.resolution = resolution

	# Differentiation

	@property
	def differentiate(self) -> None:
		return self._differentiationMethod

	@differentiate.setter
	def differentiate(self, method: str) -> None:
		if method == self.CENTRAL:
			def differential(f, x, dx):
				return (f(x + dx) - f(x - dx)) / (2 * dx)

		elif method == self.FORWARD:
			def differential(f, x, dx):
				return (f(x + dx) - f(x)) / dx

		elif method == self.BACKWARD:
			def differential(f, x, dx):
				return (f(x) - f(x - dx)) / dx

		else:
			raise NameError("Bad method for differentiation.")

		self._differentiationMethod = differential

	@differentiate.getter
	def differentiate(self):
		if self._differentiationMethod == None:
			raise RuntimeError("Can\'t differentiate without setting a differentiation method.")
		return self._differentiationMethod

	# Integration

	@property
	def integrate(self) -> None:
		return self._integrationMethod

	@integrate.setter
	def integrate(self, method: str) -> None:
		if method == self.TRAPEZOIDAL:
			def integral(f, a, b, n):
				dx = (b - a) / n
				s = 0.5 * (f(a) + f(b))
				for i in range(1, n):
					s += f(a + i * dx)
				return s * dx

		if method == self.SIMPSON:
			def integral(f, a, b, n):
				dx = (b - a) / n
				s = f(a) + f(b)
				for i in range(1, n, 2):
					s += 4 * f(a + i * dx)
				for i in range(2, n-2, 2):
					s += 2 * f(a + i * dx)
				s *= dx / 3
				return s

		else:
			raise NameError("Bad method for integration.")

		self._integrationMethod = integral

	@integrate.getter
	def integrate(self):
		if self._integrationMethod == None:
			raise RuntimeError("Can\'t integrate without setting an integration method.")
		return self._integrationMethod


class ExtendedCalculus(Calculus):
	def integrateLineSegment(self, f: Callable[[Vector], Scalar], a: Vector, b: Vector, n) -> Scalar:
		dV = b - a
		g = lambda x: f(a + x * dV)
		return self.integrate(g, 0, 1, n)
