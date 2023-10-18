from typing import Union
from typing import Iterable
from typing import Tuple
from typing import Any
from typing import Callable

from math import sqrt
from math import acos

from decimal import Decimal

import sys

from abc import ABC
from abc import abstractmethod

Scalar = Union[int, float, Decimal]

def sgn(x: Scalar) -> int:
	if x > 0:
		return 1
	if x < 0:
		return -1
	return 0

class ProgressBar:
	def __init__(self, iterable, label: str="Processing: ", length=None, fillchar='#', width=100):
		self.iterable = iterable
		self.length = length if length is not None else len(iterable)
		self.fillchar = fillchar
		self.width = width
		self.label = label

	def __iter__(self):
		self.progress = 0
		self.iterator = iter(self.iterable)
		return self

	def __next__(self):
		try:
			item = next(self.iterator)
		except StopIteration:
			sys.stdout.write('\n')
			raise StopIteration

		self.progress += 1
		percentage = self.progress / self.length
		filledwidth = int(self.width * percentage)
		bar = f'{self.fillchar * filledwidth}{" " * (self.width - filledwidth)}'
		sys.stdout.write('\r' + self.label + f'[{bar}] {percentage * 100:.1f}%')
		sys.stdout.flush()

		del percentage
		del filledwidth
		del bar

		return item

class Vector:

	"""
	Vector class, supporting most fundamental vector operations.
	"""

	def __init__(self, x: Scalar, y: Scalar, z: Scalar) -> None:
		self.x, self.y, self.z = Decimal(x), Decimal(y), Decimal(z)

	def __repr__(self) -> str:
		return "<" + ", ".join(map(str, self)) + ">"

	def __abs__(self) -> Scalar:
		return Decimal(sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2)))

	def __iter__(self) -> Iterable[Scalar]:
		return iter((self.x, self.y, self.z))

	def __eq__(self, other: "Vector") -> bool:
		if type(other) != Vector:
			return False
		return (self.x, self.y, self.z) == (other.x, other.y, other.z)

	def __neq__(self, other: "Vector") -> bool:
		return not (self == other)

	# Vector operations

	def dot(self, other: "Vector") -> Scalar:
		return Decimal(sum([xn * yn for xn, yn in zip(self, other)]))

	def cross(self, other: "Vector") -> "Vector":
		return Vector(
			x = Decimal(self.y * other.z) - Decimal(self.z * other.y),
			y = Decimal(self.x * other.z) - Decimal(self.z * other.x),
			z = Decimal(self.x * other.y) - Decimal(self.y * other.x)
		)

	def angle(self, other: "Vector") -> Scalar:
		return Decimal(acos((Vector.dot(self, other)) / (abs(self) * abs(other))))

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
			x = self.x * Decimal(factor),
			y = self.y * Decimal(factor),
			z = self.z * Decimal(factor)
		)

	def __truediv__(self, factor: Scalar) -> "Vector":
		return Vector(
			x = self.x / Decimal(factor),
			y = self.y / Decimal(factor),
			z = self.z / Decimal(factor)
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

	def __neg__(self) -> "Vector":
		return self * -1

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

	def toPolar(self) -> "Vector":
		r = abs(self)
		theta = self.z / r
		phi = sgn(self.y) * self.x / sqrt((self.x ** 2) + (self.y ** 2))

Value = Union[Scalar, Vector]

class Calculus:

	def __init__(self, h: Scalar=Decimal(0.000001)) -> None:
		self.h = Decimal(h)

		self.dx = Vector(self.h, 0, 0)
		self.dy = Vector(0, self.h, 0)
		self.dz = Vector(0, 0, self.h)

	def differential(self, f: Callable[[Scalar], Scalar], x: Scalar=None) -> Scalar:
		"""
		Use the definition of a derivative to perform differentiation.
		"""

		def differential(y: Scalar) -> Scalar:
			return (f(y + self.h) - f(y)) / self.h
		
		if x == None:
			return differential
		
		return Decimal(differential(x))
	
	def integral(self, f: Callable[[Scalar], Scalar], a: Scalar=None, b: Scalar=None) -> Scalar:
		"""
		Perform procedural integration (may take a long time depending on h).
		"""

		def integrate(j: Scalar, k: Scalar) -> Scalar:
			if j == k:
				return Decimal(0)
			
			if j > k:
				return integrate(f, k, j)
			
			i = 0
			x = j

			while x < k:
				i += f(x) * self.h
				x += self.h

			return i

		if None in (a, b):
			return integrate
		
		return Decimal(integrate(a, b))
	
	def curveIntegral(self, f: Callable[[Vector], Scalar], c: Callable[[Scalar], Vector], a: Scalar=None, b: Scalar=None) -> Scalar:
		"""
		Integrate over a parameterized curve.
		"""

		def integrateCurve(j: Scalar, k: Scalar) -> Scalar:
			i = 0
			x = j

			while x < k:
				i += f(c(x)) * self.h 
				x += self.h

			return i
		
		if None in (a, b):
			return integrateCurve
		
		return integrateCurve(a, b)
	
	def lineIntegral(self, f: Callable[[Vector], Scalar], a: Vector=None, b: Vector=None) -> Scalar:
		"""
		Integrate over a line - essentially a high-level Calculus.curveIntegral
		"""
		
		def lineIntegral(x: Vector, y: Vector) -> Scalar:
			dx = y - x
			c = lambda p: x + (dx * p)
			return self.curveIntegral(f, c, 0, 1)
		
		if None in (a, b):
			return lineIntegral
		
		return lineIntegral(a, b)

	def gradient(self, f: Callable[[Vector], Scalar], v: Vector=None) -> Vector:
		"""
		The gradient of a scalar field is a vector field giving
		the magnitude and direction of maximum increase at a given point.
		"""
		
		def gradientField(u: Vector) -> Vector:
			return Vector(
				(f(u + self.dx) - f(u)) / self.h,
				(f(u + self.dy) - f(u)) / self.h,
				(f(u + self.dz) - f(u)) / self.h,
			)

		if v == None:
			return gradientField

		return gradientField(v)

	def divergence(self, f: Callable[[Vector], Vector], v: Vector=None) -> Scalar:
		"""
		The divergence of a vector field is a scalar field
		associated with the vector field's tendency to diverge
		to or from a given point.
		"""

		def divergenceField(u: Vector) -> Scalar:
			return Decimal(sum((
				((f(u + self.dx) - f(u)) / self.h).x,
				((f(u + self.dy) - f(u)) / self.h).y,
				((f(u + self.dz) - f(u)) / self.h).z
			)))

		if v == None:
			return divergenceField

		return divergenceField(v) 
	
	def curl(self, f: Callable[[Vector], Vector], v: Vector=None) -> Vector:
		"""
		The curl of a vector field is another vector field that roughly
		gives the magnitude of angular torque that would be applied to a 
		tiny pinwheel placed in the first vector field.
		"""

		def curlField(u: Vector) -> Vector:
			i = f(u)

			dzdy = ((f(u + self.dy) - i) / self.h).z
			dydz = ((f(u + self.dz) - i) / self.h).y

			dxdz = ((f(u + self.dz) - i) / self.h).x
			dzdx = ((f(u + self.dx) - i) / self.h).z

			dydx = ((f(u + self.dx) - i) / self.h).y
			dxdy = ((f(u + self.dy) - i) / self.h).x

			return Vector(
				x = dzdy - dydz,
				y = dxdz - dzdx,
				z = dydx - dxdy
			)
	
		if v == None:
			return curlField
		
		return curlField(v)

class SystemFailure(BaseException):
	NONFATAL = "NONFATAL"
	FATAL = "FATAL"

	def __init__(self, fatality: str, error: str, description: str) -> None:
		BaseException.__init__(self, error)
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
