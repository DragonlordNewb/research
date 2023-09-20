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

Scalar = Union[float, int]

# ===== Masses and Bodies ===== #

class Vector:
	def __init__(self, x, y, z) -> None:
		self.x, self.y, self.z = x, y, z

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

	def magnitude(self) -> Scalar:
		return sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	@classmethod
	@cache
	def zero(cls) -> "Vec3":
		return cls(0, 0, 0)

	@cache
	def normal(self) -> "Vec3":
		return Vec3(
			x=self.x / self.magnitude(),
			y=self.y / self.magnitude(),
			z=self.z / self.magnitude()
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
	
class PointMass:
	"""
	A Python representation of a point mass.
	"""

	def __init__(self, location: Vector, energy: Scalar) -> None:
		self.location = location
		self.energy = energy

class Body(ABC):
	"""
 	A Python representation of a physical object.
	
	Functionally approximated as a set of point masses.
	"""

	location = Vector.zero()
	velocity = Vector.zero()

	@abstractmethod
	def points(self) -> Iterable[PointMass]:
		pass

	def center(self) -> Vector:
		return Vector.mean(*self.points)

# ===== Spacetime ===== #

class Force(ABC):
	"""
	A Python representation of a force (like electromagnetism,
	gravitational, etc.). 

	Must be abstracted to add the actual acceleration parameters.
	The abstracted method must accept the two PointMass objects and
	return two linear acceleration Vectors.
	"""

	@abstractmethod
	def act(self, p1: PointMass, p2: PointMass) -> tuple[Vector, Vector]:
		pass

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

	def __init__(self, metric: Metric, step=0.000000001) -> None:
		self.metric = metric
		self.metric.spacetime = self

	def update(self, times: int=1) -> None:
		"""
		Move the simulation forward in time by "times" timesteps.
		"""

		# Iterate to update the right number of times
		if times > 1:
			for _ in range(times - 1):
				self.update(times=1)

		for 
