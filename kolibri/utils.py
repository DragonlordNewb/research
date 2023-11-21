import sys
import decimal
from decimal import Decimal
from math import *
from typing import Union
from typing import Iterable
from typing import Callable
from typing import Any

decimal.getcontext().prec = 12

Scalar = Union[float, int, Decimal]

class ProgressBar:
	def __init__(self, iterable, total=None, length=50, prefix='Progress:', suffix='', fill='#', print_end='\r'):
		self.iterable = iterable
		self.total = total if total is not None else len(iterable)
		self.length = length
		self.prefix = prefix
		self.suffix = suffix
		self.fill = fill
		self.print_end = print_end
		self.current_iteration = 0
	
	def update(self, progress):
		filled_length = int(self.length * progress // self.total)
		bar = self.fill * filled_length + '-' * (self.length - filled_length)
		percent = progress / self.total * 100
		self.print(f'{self.prefix} |{bar}| {percent:.2f}% {self.suffix}', end=self.print_end)
	
	def print(self, text, end='\n'):
		sys.stdout.write(text)
		sys.stdout.flush()
		sys.stdout.write(end)
		sys.stdout.flush()
	
	def __iter__(self):
		for item in self.iterable:
			yield item
			self.current_iteration += 1
			self.update(self.current_iteration)
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		sys.stdout.write('\n')  # Move to the next line after the progress bar is complete

class Vec3:

	"""
	Vec3 class, supporting most fundamental vector operations.
	"""

	def __init__(self, x: Scalar=Decimal(0), y: Scalar=Decimal(0), z: Scalar=Decimal(0)) -> None:
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

	def __init__(self, t: Scalar=Decimal(0), x: Scalar=Decimal(0), y: Scalar=Decimal(0), z: Scalar=Decimal(0)) -> None:
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