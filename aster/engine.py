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

from aster import constants

Scalar = Union[float, int]

# ===== Masses and Bodies ===== #

class Vector:
	def __init__(self, x, y, z) -> None:
		self.x, self.y, self.z = x, y, z

	def __iter__(self) -> Iterable[Scalar]:
		return iter((self.x, self.y, self.z))
	
	# Addition

	@classmethod
	def sum(cls, *vectors: tuple["Vector"]) -> "Vector":
		return cls(
			x = sum([v.x for v in vectors]),
			y = sum([v.y for v in vectors]),
			z = sum([v.z for v in vectors])
		)

	def __add__(self, other: "Vector") -> "Vector":
		return Vector.sum(self, other)

	def __iadd__(self, other: "Vector") -> "Vector":
		return self + other

	# Dot product

	def dot(self, other) -> Scalar:
		return sum([a * b for a, b in zip(self, other)])

	def __mul__(self, other) -> Scalar:
		return self.dot(other)
	
	# Cross product

	def cross(self, other) -> "Vector":
		return type(self)(
			x = (self.y * other.z) - (self.z * other.y),
			y = (self.x * other.z) - (self.z * other.x),
			z = (self.x * other.y) - (self.y * other.x)
		)
	
	def __matmul__(self, other) -> "Vector":
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

	def magnitude(self) -> Scalar:
		return sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	@classmethod
	@cache
	def zero(cls) -> "Vector":
		return cls(0, 0, 0)

	@cache
	def normal(self) -> "Vec3":
		return Vec3(
			x=self.x / self.magnitude(),
			y=self.y / self.magnitude(),
			z=self.z / self.magnitude()
		)

	@classmethod
	def mean(cls, *vectors: tuple["Vector"]) -> "Vector":
		l = len(vectors)
		return cls(
			x=sum([v.x for v in vectors]) / l,
			y=sum([v.y for v in vectors]) / l,
			z=sum([v.z for v in vectors]) / l
		)

	def scale(self, factor: Scalar) -> "Vector":
		return Vec3(x * factor, y * factor, z * factor)

	def scaleInPlace(self, factor: Scalar) -> "Vector":
		v = self.scale(factor)
		self.x, self.y, self.z = v
		return v
	
class PointObject:
	"""
	A Python representation of a point object, i.e. that occupies no volume.
	"""

	location = Vector.zero()

	def __init__(self, **kwargs: dict[str, Any]) -> None:
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])
		self.data = kwargs

class Body(ABC):
	"""
 	A Python representation of a physical object.
	
	Functionally approximated as a set of point masses.
	"""

	location = Vector.zero()
	velocity = Vector.zero()

	def __init__(self, **kwargs: dict[str, Any]) -> None:
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])
		self.data = kwargs

		self.hash = randbytes(8)

	def __iter__(self) -> Iterable[PointObject]:
		return iter(self.points())

	@cache
	def __hash__(self) -> int:
		s = 0
		for index, byte in enumerate(self.hash):
			s += (256 ** index) * byte
		return s
	
	def __eq__(self, other: "Body") -> bool:
		return hash(self) == hash(other)

	@abstractmethod
	def points(self) -> Iterable[PointObject]:
		pass

	def center(self) -> Vector:
		return Vector.mean(*self.points)

# ===== Spacetime ===== #

class Metric(ABC):
	"""
 	A Python representation of a spacetime metric.
  	Must adequately be subclassed to describe how an
   	object experiences time dilation, space contraction,
    etc.
    """

	spacetime: "Spacetime" = None

	@abstractmethod
	def timeDilation(self, body: Body) -> Scalar:
		"""
		By what factor will the body's experience of time be slowed?
		"""
		pass
	
	@abstractmethod
	def spaceContraction(self, body: Body) -> Scalar:
		"""
		By what factor will the body's experience of space be contracted?
		"""
		pass

class Force(ABC):
	"""
	A Python representation of a force (like electromagnetism,
	gravitational, etc.). 

	Must be abstracted to add the actual acceleration parameters.
	The abstracted method must accept the two PointObject objects and
	return two linear acceleration Vectors.
	"""

	@abstractmethod
	def act(self, metric: Metric, p1: PointObject, p2: PointObject) -> tuple[Vector, Vector]:
		pass

class Spacetime:
	"""
 	A Python representation of spacetime.

 	Requires a single parameter, "metric", which
	must be an aster.engine.Metric object. This metric
 	will govern the behavior of the spacetime's geometry.

	Optionally takes a second parameter, "step", which is 
	the integration timestep; that is, every one "update" 
	call of the Spacetime will tick everything in the
	simulation forward by that many seconds (or microseconds
	or years or however long "step" is). "step" defaults to
	one nanosecond for very high resolution simulations.

	Optionally takes any number of parameters after that which
	must all be Force objects, and these are the forces that will
	act upon objects in the simulation.
	"""

	def __init__(self, metric: Metric, step=0.000000001, *forces: tuple[Force]) -> None:
		self.metric = metric
		self.metric.spacetime = self
		self.step = step
		self.objects = []
		self.forces = forces

	def __iter__(self) -> Iterable[Body]:
		return iter(self.objects)

	def update(self, times: int=1) -> None:
		"""
		Move the simulation forward in time by "times" timesteps.
		"""

		# Iterate to update the right number of times
		if times > 1:
			for _ in range(times - 1):
				self.update(times=1)

		accelerations = {body: Vector.zero() for body in self}

		for body1 in self:
			for body2 in self:
				# don't let objects interact with themselves - that could become problematic
				if body1 == body2:
					continue

				for pointObject1 in body1:
					for pointObject2 in body2:

						for force in self.forces:
							accel1, accel2 = force.act(self.metric, pointObject1, pointObject2)
						
						accelerations[body1] += accel1
						accelerations[body2] += accel2

		correctedAccelerations = {
			body: accelerations[body] * self.metric.timeDilation(body) * self.step
			for body in self
		}

		for body in self:
			body.velocity += correctedAccelerations[body]
			body.location += body.velocity * self.metric.spaceContraction(body)