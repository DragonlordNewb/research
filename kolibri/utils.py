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
		return (f(v + Vector(self.h, 0, 0)) - i) / self.h

	def divergence(self, f: Callable[[Vector], Scalar], v: Vector) -> Vector:
		g = self.gradient(f, v)
		return g.x + g.y + g.z
	
class SystemFailure(Exception):
	NONFATAL = "NONFATAL"
	FATAL = "FATAL"

	def __init__(self, fatality: str, error: str, description: str) -> None:
		Exception.__init__(self, error)
		self.error = error
		self.description = description
		self.fatality = fatality

	def panic(self) -> Exception:
		print(self.fatality + " SYSTEM FAILURE: " + self.error)
		print("\t" + self.description.replace("\n", "\t\n"))
		if self.fatality == self.FATAL:
			raise self

# antired = cyan
# antigreen = purple
# antiblue = yellow

_GellMann__isqrt3 = 1/sqrt(3)

class GellMann:

	MATRICES = {
	# L_1: red and cyan
	1: [
		[0, 1, 0],
		[1, 0, 0], 
		[0, 0, 0]
	],

	# L_2: green and purple
	2: [
		[0,  -1j, 0],
		[1j, 0,   0],
		[0,  0,   0]
	],

	# L_3: blue and yellow
	3: [
		[1, 0,  0],
		[0, -1, 0],
		[0, 0,  0]
	],

	# L_4: red, cyan, green or red, cyan, purple
	4: [
		[0, 0, 1],
		[0, 0, 0],
		[1, 0, 0]
	],

	# L_5: red, cyan, blue red, cyan, yellow
	5: [
		[0,  0, -1j],
		[0,  0, 0  ],
		[1j, 0, 0  ]
	],

	# L_6: green, purple, blue or green, purple, yellow
	6: [
		[0, 0, 0],
		[0, 0, 1],
		[0, 1, 0]
	],

	# L_7: blue, yellow, red or blue, yellow, cyan
	7: [
		[0, 0,  0  ],
		[0, 0,  -1j],
		[0, 1j, 0  ]
	],

	# L_8: red, green, blue or cyan, purple, yellow
	8: [
		[__isqrt3, 0,        0            ],
		[0,        __isqrt3, 0            ],
		[0,        0,        -2 * __isqrt3]
	]
}

	def __init__(self, index: int) -> None:
		self.index = index
		self.matrix = self.MATRICES[index] 

	def __mul__(self, other: "GellMann") -> Scalar:
		matrix1 = self.matrix
		matrix2 = other.matrix
		p1 = self.multiply3x3(matrix1, matrix2)
		p2 = self.multiply3x3(matrix2, matrix1)
		s = self.add3x3(p1, p2)

	@staticmethod
	def add3x3(matrix1: list[list[Scalar]], matrix2: list[list[Scalar]]) -> list[list[Scalar]]:
		return [[matrix1[r][c] + matrix2[r][c] for c in range(3)] for r in range(3)]

	@staticmethod
	def multiply3x3(matrix1: list[list[Scalar]], matrix2: list[list[Scalar]]) -> list[list[Scalar]]:
		((a, b, c), (d, e, f), (g, h, i)) = matrix1
		((j, k, l), (m, n, o), (p, q, r)) = matrix2
		return [
			[(a * j) + (b * m) + (c * p), (a * k) + (b * n) + (c * q), (a * l) + (b * o) + (c * r)],
			[(d * j) + (e * m) + (f * p), (d * k) + (e * n) + (f * q), (d * l) + (e * o) + (f * r)],
			[(g * j) + (h * m) + (i * p), (g * k) + (h * n) + (i * q), (g * l) + (h * o) + (i * r)]
		]