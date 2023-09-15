from abc import ABC
from abc import abstractmethod

from functools import cache

from math import sqrt
from math import sin
from math import asin
from math import cos
from math import acos
from math import tan
from math import atan

from typing import Union
from typing import Any
from typing import Iterable

from random import randbytes

from stem1 import constants

Scalar = Union[float, int]

class Vec3:
	def __init__(self, x, y, z) -> None:
		self.x, self.y, self.z = x, y, z
		self.magnitude = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def __iter__(self) -> Iterable[Scalar]:
		return iter((self.x, self.y, self.z))

	# Dot product

	def dot(self, other) -> Scalar:
		return sum([a * b for a, b in zip(self, other)])

	def __mul__(self, other) -> Scalar:
		return self.dot(other)
	
	# Cross product

	def cross(self, other) -> "Vec3":
		return type(self)(
			x = (self.y * other.z) - (self.z * other.y),
			y = (self.x * other.z) - (self.z * other.x),
			z = (self.x * other.y) - (self.y * other.x)
		)
	
	def __matmul__(self, other) -> "Vec3":
		return self.cross(other)

	# Distance and angle

	def distance(self, other) -> Scalar:
		return sqrt(
			((self.x - other.x) ** 2) + \
			((self.y - other.y) ** 2) + \
			((self.z - other.z) ** 2)
		)
	
	def angle(self, other) -> Scalar:
		return acos((self * other) / (self.magnitude() * other.magnitude()))
	
	# Miscellaneous

	def normal(self) -> "Vec3":
		return Vec3(
			x=self.x / self.magnitude,
			y=self.y / self.magnitude,
			z=self.z / self.magnitude
		)

	@classmethod
	def mean(cls, *vectors: tuple["Vec3"]) -> "Vec3":
		l = len(vectors)
		return cls(
			x=sum([v.x for v in vectors]) / l,
			y=sum([v.y for v in vectors]) / l,
			z=sum([v.z for v in vectors]) / l
		)

	def scale(self, factor: Scalar) -> "Vec3":
		return Vec3(x * factor, y * factor, z * factor)

# ===== Objects ===== #

class Object(ABC):
	def __init__(self, energy: Scalar=1, charge: Scalar=0, **kwargs: dict[str, Any]) -> None:
		self.energy, self.charge = energy, charge
		self.baseEnergy = energy
		self.linearPosition = Vec3(0, 0, 0)
		self.angularPosition = Vec3(0, 0, 0)
		self.linearVelocity = Vec3(0, 0, 0)
		self.angularVelocity = Vec3(0, 0, 0)
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])
		self.id = randbytes(16)

	def __eq__(self, other) -> bool:
		return self.id == other.id
	
	def __neq__(self, other) -> bool:
		return not (self == other)

	@abstractmethod
	def points(self) -> Iterable[Vec3]:
		raise NotImplementedError

	def center(self) -> Vec3:
		return Vec3.mean(*self.points())

class Particle(Object):
	def points(self) -> tuple[Vec3]:
		return self.linearPosition

# ===== Forces ===== #

class Force(ABC):
	def __init__(self, kwargs: dict[str, Any]) -> None:
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])

	@abstractmethod
	def act(self, a: Object, b: Object) -> tuple[Vec3, Vec3]:
		raise NotImplementedError
	
class Gravitional(Force):
	def act(self, a: Object, b: Object) -> tuple[Vec3, Vec3, Vec3, Vec3]:
		# return an (lin. accel 1, ang. accel 1, lin. accel 2, ang. accel 2)
		pass

# ===== Spacetime ===== #

class Metric:
	def __init__(self):
		pass

class Spacetime:
	def __init__(self, metric: Metric, *forces: tuple[Force], step: Scalar=0.00001) -> None:
		self.objects = []
		self.step = step
		self.forces = forces
		self.metric = metric

	def __iter__(self) -> Iterable[Object]:
		return iter(self.objects)

	def tick(self) -> None:
		for object1 in self:
			for object2 in self:
				if object1 != object2:
					for force in self.forces:
						lin1, ang1, lin2, ang2 = force.act(object1, object2)
						for object, lin, ang in [(object1, lin1, ang1), (object2, lin2, ang2)]:
							dilation = metric.dilation(self, object)
							object.linearVelocity += lin * self.step * dilation
							object.angularVelocity += ang * self.step * dilation

							object.linearPosition += object.linearVelocity * self.step * dilation
							object.angularPosition += object.angularVelocity * self.step * dilation

							object.energy = metric.energy(object)
