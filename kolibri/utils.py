# not even gonna try and put comments on this one
#
# so
#
# if it isn't intuitive from the get go, documentation
# for kolibri.utils can be found in hell (ask Asmodeus 
# first once you get there)

from typing import Union
from typing import Iterable
from typing import Any
from typing import Callable
from typing import Tuple
from abc import ABC
from abc import abstractmethod
from abc import abstractclassmethod
from abc import abstractstaticmethod

from math import sqrt
from math import acos

from decimal import Decimal

import sys

Scalar = Union[Decimal, int, float]

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

class Vec3:

	"""
	Vec3 class, supporting most fundamental vector operations.
	"""

	def __init__(self, x: Scalar, y: Scalar, z: Scalar) -> None:
		self.x, self.y, self.z = Decimal(x), Decimal(y), Decimal(z)

	def __repr__(self) -> str:
		return "<" + ", ".join(map(str, self)) + ">"

	def __abs__(self) -> Scalar:
		return Decimal(sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2)))

	def __iter__(self) -> Iterable[Scalar]:
		return iter((self.x, self.y, self.z))

	def __eq__(self, other: "Vec3") -> bool:
		if type(other) != Vec3:
			return False
		return (self.x, self.y, self.z) == (other.x, other.y, other.z)

	def __neq__(self, other: "Vec3") -> bool:
		return not (self == other)

	def __getitem__(self, index: int) -> Scalar:
		return list(self)[index]

	def __setitem__(self, index: int, value: Scalar) -> None:
		if index == 0:
			self.x = Decimal(value)
		elif index == 1:
			self.y = Decimal(value)
		elif index == 2:
			self.z = Decimal(value)
		else:
			raise IndexError("Vec3s only go up to index 2.")

	# Vec3 operations

	def dot(self, other: "Vec3") -> Scalar:
		return Decimal(sum([xn * yn for xn, yn in zip(self, other)]))

	def cross(self, other: "Vec3") -> "Vec3":
		return Vec3(
			x = Decimal(self.y * other.z) - Decimal(self.z * other.y),
			y = Decimal(self.x * other.z) - Decimal(self.z * other.x),
			z = Decimal(self.x * other.y) - Decimal(self.y * other.x)
		)

	def angle(self, other: "Vec3") -> Scalar:
		return Decimal(acos((Vec3.dot(self, other)) / (abs(self) * abs(other))))

	def normal(self) -> "Vec3":
		return self / abs(self)

	# Basic operations

	def __add__(self, other: "Vec3") -> "Vec3":
		return Vec3(
			x = self.x + other.x,
			y = self.y + other.y,
			z = self.z + other.z
		)

	def __sub__(self, other: "Vec3") -> "Vec3":
		return Vec3(
			x = self.x - other.x,
			y = self.y - other.y,
			z = self.z - other.z
		)

	def __mul__(self, factor: Scalar) -> "Vec3":
		return Vec3(
			x = self.x * Decimal(factor),
			y = self.y * Decimal(factor),
			z = self.z * Decimal(factor)
		)

	def __truediv__(self, factor: Scalar) -> "Vec3":
		return Vec3(
			x = self.x / Decimal(factor),
			y = self.y / Decimal(factor),
			z = self.z / Decimal(factor)
		)

	def __iadd__(self, other: "Vec3") -> "Vec3":
		return self + other

	def __isub__(self, other: "Vec3") -> "Vec3":
		return self - other

	def __imul__(self, other: Scalar) -> "Vec3":
		return self * other

	def __rmul__(self, other: Scalar) -> "Vec3":
		return self * other

	def __itruediv__(self, other: "Vec3") -> "Vec3":
		return self / other

	def __neg__(self) -> "Vec3":
		return self * -1

	# Miscellaneous

	@staticmethod
	def mean(*vectors: tuple["Vec3"]) -> "Vec3":
		v = Vec3(0, 0, 0)
		for vector in vectors:
			v += vector
		return v

	@staticmethod
	def weightedMean(vectors: Iterable["Vec3"], weights: Iterable[Scalar]) -> "Vec3":
		weightedSum = Vec3(0, 0, 0)
		totalWeight = sum(weights)

		for vector, weight in zip(vectors, weights):
			weightedSum += vector * weight

		return weightedSum / totalWeight

	@classmethod
	def zero(cls) -> "Vec3":
		return cls(0, 0, 0)

	def toPolar(self) -> "Vec3":
		r = abs(self)
		theta = self.z / r
		phi = sgn(self.y) * self.x / sqrt((self.x ** 2) + (self.y ** 2))

class Vec4:

	"""
	Vec3 class, supporting most fundamental vector operations.
	"""

	def __init__(self, t: Scalar, x: Scalar, y: Scalar, z: Scalar) -> None:
		self.t, self.x, self.y, self.z = Decimal(t), Decimal(x), Decimal(y), Decimal(z)

	def __repr__(self) -> str:
		return "<" + ", ".join(map(str, self)) + ">"

	def __abs__(self) -> Scalar:
		return Decimal(sqrt((self.t ** 2) * (self.x ** 2) + (self.y ** 2) + (self.z ** 2)))

	def __iter__(self) -> Iterable[Scalar]:
		return iter((self.t, self.x, self.y, self.z))

	def __eq__(self, other: "Vec4") -> bool:
		if type(other) != Vec3:
			return False
		return (self.t, self.x, self.y, self.z) == (self.t, other.x, other.y, other.z)

	def __neq__(self, other: "Vec4") -> bool:
		return not (self == other)

	def __getitem__(self, index: int) -> Scalar:
		return list(self)[index]

	def __setitem__(self, index: int, value: Scalar) -> None:
		if index == 0:
			self.t = Decimal(value)
		elif index == 1:
			self.x = Decimal(value)
		elif index == 2:
			self.y = Decimal(value)
		elif index == 3:
			self.z = Decimal(value)
		else:
			raise IndexError("Vec4s only go up to index 3.")

	# Vec4 operations

	def spatial(self) -> "Vec3":
		return Vec3(self.x, self.y, self.z)

	def dot(self, other: "Vec4") -> Scalar:
		return Decimal(sum([xn * yn for xn, yn in zip(self, other)]))

	def angle(self, other: "Vec4") -> Scalar:
		return Decimal(acos((Vec4.dot(self, other)) / (abs(self) * abs(other))))

	def normal(self) -> "Vec4":
		return self / abs(self)

	# Basic operations

	def __add__(self, other: "Vec3") -> "Vec4":
		return Vec4(
			t = self.t + other.t,
			x = self.x + other.x,
			y = self.y + other.y,
			z = self.z + other.z
		)

	def __sub__(self, other: "Vec3") -> "Vec4":
		return Vec4(
			t = self.t - other.t,
			x = self.x - other.x,
			y = self.y - other.y,
			z = self.z - other.z
		)

	def __mul__(self, factor: Scalar) -> "Vec4":
		return Vec4(
			t = self.t * Decimal(factor),
			x = self.x * Decimal(factor),
			y = self.y * Decimal(factor),
			z = self.z * Decimal(factor)
		)

	def __truediv__(self, factor: Scalar) -> "Vec4":
		return Vec4(
			t = self.t / Decimal(factor),
			x = self.x / Decimal(factor),
			y = self.y / Decimal(factor),
			z = self.z / Decimal(factor)
		)

	def __iadd__(self, other: "Vec4") -> "Vec4":
		return self + other

	def __isub__(self, other: "Vec4") -> "Vec4":
		return self - other

	def __imul__(self, other: Scalar) -> "Vec4":
		return self * other

	def __rmul__(self, other: Scalar) -> "Vec4":
		return self * other

	def __itruediv__(self, other: "Vec4") -> "Vec4":
		return self / other

	def __neg__(self) -> "Vec4":
		return self * -1

	# Miscellaneous

	@staticmethod
	def mean(*vectors: tuple["Vec4"]) -> "Vec4":
		v = Vec4(0, 0, 0, 0)
		for vector in vectors:
			v += vector
		return v

	@staticmethod
	def weightedMean(vectors: Iterable["Vec4"], weights: Iterable[Scalar]) -> "Vec4":
		weightedSum = Vec4(0, 0, 0, 0)
		totalWeight = sum(weights)

		for vector, weight in zip(vectors, weights):
			weightedSum += vector * weight

		return weightedSum / totalWeight

	@classmethod
	def zero(cls) -> "Vec3":
		return cls(0, 0, 0, 0)

class Vector:
	
	"""
	General Vector. Auto-subclasses.
	"""

	def __init__(self, a=0, b=0, c=0, d=None):
		if d == None:
			Vec3.__init__(self, a, b, c)
		else:
			Vec4.__init__(self, a, b, c, d)

	@classmethod
	def zero(cls, dimension: int) -> Union["Vec3", "Vec4"]:
		if dimension == 4:
			return Vec4(0, 0, 0, 0)
		elif dimension == 3:
			return Vec3(0, 0, 0)
		raise IndexError("Bad number of dimensions.")

Value = Union[Scalar, Vec3]

class Calculus:

	def __init__(self, h: Scalar=Decimal(0.000001)) -> None:
		self.h = Decimal(h)

		self.dx = Vec3(self.h, 0, 0)
		self.dy = Vec3(0, self.h, 0)
		self.dz = Vec3(0, 0, self.h)

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
	
	def curveIntegral(self, f: Callable[[Vec3], Scalar], c: Callable[[Scalar], Vec3], a: Scalar=None, b: Scalar=None) -> Scalar:
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
	
	def lineIntegral(self, f: Callable[[Vec3], Scalar], a: Vec3=None, b: Vec3=None) -> Scalar:
		"""
		Integrate over a line - essentially a high-level Calculus.curveIntegral
		"""
		
		def lineIntegral(x: Vec3, y: Vec3) -> Scalar:
			dx = y - x
			c = lambda p: x + (dx * p)
			return self.curveIntegral(f, c, 0, 1)
		
		if None in (a, b):
			return lineIntegral
		
		return lineIntegral(a, b)

	def gradient(self, f: Callable[[Vec3], Scalar], v: Vec3=None) -> Vec3:
		"""
		The gradient of a scalar field is a vector field giving
		the magnitude and direction of maximum increase at a given point.
		"""
		
		def gradientField(u: Vec3) -> Vec3:
			return Vec3(
				(f(u + self.dx) - f(u)) / self.h,
				(f(u + self.dy) - f(u)) / self.h,
				(f(u + self.dz) - f(u)) / self.h,
			)

		if v == None:
			return gradientField

		return gradientField(v)

	def divergence(self, f: Callable[[Vec3], Vec3], v: Vec3=None) -> Scalar:
		"""
		The divergence of a vector field is a scalar field
		associated with the vector field's tendency to diverge
		to or from a given point.
		"""

		def divergenceField(u: Vec3) -> Scalar:
			return Decimal(sum((
				((f(u + self.dx) - f(u)) / self.h).x,
				((f(u + self.dy) - f(u)) / self.h).y,
				((f(u + self.dz) - f(u)) / self.h).z
			)))

		if v == None:
			return divergenceField

		return divergenceField(v) 
	
	def curl(self, f: Callable[[Vec3], Vec3], v: Vec3=None) -> Vec3:
		"""
		The curl of a vector field is another vector field that roughly
		gives the magnitude of angular torque that would be applied to a 
		tiny pinwheel placed in the first vector field.
		"""

		def curlField(u: Vec3) -> Vec3:
			i = f(u)

			dzdy = ((f(u + self.dy) - i) / self.h).z
			dydz = ((f(u + self.dz) - i) / self.h).y

			dxdz = ((f(u + self.dz) - i) / self.h).x
			dzdx = ((f(u + self.dx) - i) / self.h).z

			dydx = ((f(u + self.dx) - i) / self.h).y
			dxdy = ((f(u + self.dy) - i) / self.h).x

			return Vec3(
				x = dzdy - dydz,
				y = dxdz - dzdx,
				z = dydx - dxdy
			)
	
		if v == None:
			return curlField
		
		return curlField(v)
		
	def laplacian(self, f: Callable[[Vec3], Scalar], v: Vec3=None) -> Scalar:
		"""
  		The Laplacian of a scalar field is the divergence of its gradient.
  		"""
		
		def laplacianField(x: Vec3) -> Scalar:
			return self.divergence(self.gradient(f, x), x)
			
		if v == None:
			return laplacianField
			
		return laplacianField(v)