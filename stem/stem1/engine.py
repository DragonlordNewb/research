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

from time import time as epoch

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

	@classmethod
	@cache
	def zero(cls) -> "Vec3":
		return cls(0, 0, 0)

	@cache
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
	def __init__(self, name: str, energy: Scalar=1, charge: Scalar=0, **kwargs: dict[str, Any]) -> None:
		self.name = name
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
	
class LinearGravitational(Force):
	def act(self, a: Object, b: Object) -> tuple[Vec3, Vec3, Vec3, Vec3]:
		# return a (lin. accel 1, ang. accel 1, lin. accel 2, ang. accel 2)
		massA, massB = a.energy / constants.c2, b.energy / constants.c2
		dist = Vec3.distance(a.linearPosition, b.linearPosition).magnitude
		divisor = 1 / (dist ** 2)
		
		normalA = Vec3(a.x - b.x, a.y - b.y, a.z - b.z).normal()
		normalB = Vec3(b.x - a.x, b.y - a.y, b.z - a.z).normal()
		
		return (
			normalA.scale(divisor * massB * constants.G),
			Vec3.zero(),
			normalB.scale(divisor * massA * constants.G),
			Vec3.zero()
		)

# ===== Spacetime ===== #

class Metric(ABC):
	def __init__(self):
		pass
		
	@abstracmethod
	def dilation(self, *args):
		pass
		
	@abstractmethod
	def contraction(self, *args):
		pass

class Spacetime:
	def __init__(self, metric: Metric, *forces: tuple[Force], step: Scalar=0.00001) -> None:
		self.objects = []
		self.step = step
		self.forces = forces
		self.metric = metric

	def __iter__(self) -> Iterable[Object]:
		return iter(self.objects)
		
	def __getitem__(self, name: str) -> Object:
		for obj in self:
			if obj.name == name:
				return obj
		raise KeyError("No object with name " + repr(name) + ".")

	def run(self, iterations: int=1) -> None:
		if iterations != 1:
			for _ in range(iterations - 1):
				self.run(iterations=1)
				
		for object1 in self:
			for object2 in self:
				if object1 != object2:
					for force in self.forces:
						lin1, ang1, lin2, ang2 = force.act(object1, object2)
						for object, lin, ang in [(object1, lin1, ang1), (object2, lin2, ang2)]:
							dilation = metric.dilation(self, object)
							contraction = metric.contraction(self, object)
							object.linearVelocity += lin.scale(self.step * dilation)
							object.angularVelocity += ang.scale(self.step * dilation)

							object.linearPosition += object.linearVelocity.scale(self.step * dilation / contraction)
							object.angularPosition += object.angularVelocity.scale(self.step * dilation / contraction)

							object.energy = metric.energy(object)
	def runFor(self, time: Scalar) -> None:
		st = epoch()
		et = st + time
		while epoch() < et:
			self.run(1)

	def add(self, obj: Object, linearPosition: Vec3=Vec3.zero(),angularPosition: Vec3=Vec3.zero(), linearVelocity: Vec3=Vec3.zero(), angularVelocity: Vec3=Vec3.zero()) -> None:
		self.objects.append(obj)
		self[obj.name].linearPosition = linearPosition
		self[obj.name].angularPosition = angularPosition
		self[obj.name].linearVelocity = linearVelocity
		self[obj.name].angularVelocity = angularVelocity
