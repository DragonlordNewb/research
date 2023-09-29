from tkinter import Tk
from tkinter import Frame
from tkinter import Label
from tkinter import Canvas
from tkinter import Entry
from tkinter import Button

from math import sqrt
from math import pi
from math import sin
from math import cos
from math import acos

from functools import cache

from abc import ABC
from abc import abstractmethod

from typing import Callable
from typing import Iterable
from typing import Any
from typing import Union

# Mathematical constants

c = 299792458
c2 = c ** 2

# ===== Core mathematical components ===== #

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

class Calculus:

	# Differentiation methods

	CENTRAL = "central"
	FORWARD = "forward"
	BACKWARD = "backward"

	# Integration methods

	TRAPEZOIDAL = "trapezoidal"
	SIMPSON = "simpson"

	def __init__(self, resolution: int):
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
	def integrateLineSegment(self, f: Callable[[Vector], Scalar], a: Vector, b: Vector, n: int=None) -> Scalar:
		if n == None:
			n = self.resolution

		dV = b - a
		g = lambda x: f(a + (x * dV))
		return self.integrate(g, 0, 1, n) * abs(b - a)

	def gradient(self, f: Callable[[Vector], Scalar], location: Vector, d: Scalar=None) -> Vector:
		if d == None:
			d == self.resolution

		fx = lambda x: f(Vector(x, location.y, location.z))
		fy = lambda y: f(Vector(location.x, y, location.z))
		fz = lambda z: f(Vector(location.x, location.y, z))

		dfdx = self.differentiate(fx, location.x, d)
		dfdy = self.differentiate(fy, location.y, d)
		dfdz = self.differentiate(fz, location.z, d)

		return Vector(dfdx, dfdy, dfdz)

# ===== Spacetime simulation components ===== #

class Atom:
	def __init__(self, parent: "Body", location: Vector, energy: Scalar, **kwargs: dict[str, Any]) -> None:
		self.location = location
		self.energy = energy
		print(kwargs)
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])
		self.properties = list(kwargs.keys())
		self.parent = parent

	def __repr__(self) -> str:
		return "<Atom @ " + repr(self.location) + ">"

class Body(ABC):

	"""
	Generalized Python representation of an object of variable shape
	and structure.

	Supports adding properties like electric and color charge, energy,
	etc.
	"""

	def __init__(self, id: str, energy: Scalar, **kwargs: dict[str, any]) -> None:
		self.restEnergy = energy
		self.location = Vector(0, 0, 0)
		self.velocity = Vector(0, 0, 0)

		for key in kwargs.keys():
			setattr(self, key, kwargs[key])

		self.properties = kwargs

		self.id = id

	def __hash__(self) -> int:
		return hash(self.id)

	def __repr__(self) -> str:
		return "<" + type(self).__name__ + " " + repr(self.id) + ">"

	def displace(self, displacement: Vector) -> Vector:
		self.location += displacement
		return self.location

	def place(self, location: Vector) -> None:
		self.location = location

	def accelerate(self, deltaV: Vector) -> Vector:
		self.velocity += deltaV
		return self.velocity

	def impulse(self, velocity: Vector) -> None:
		self.velocity = velocity

	@abstractmethod
	def atoms(self) -> Iterable[Atom]:
		return NotImplementedError

	def centerOfMass(self) -> Vector:
		if len(self.atoms()) == 1:
			return self.atoms()[0].location

		vecs = []
		weights = []
		for atom in self.atoms():
			vecs.append(atom.location)
			weights.append(atom.energy)

		return Vector.weightedMean(vecs, weights)

	def apply(self, force: Vector) -> None:
		self.velocity += force / (self.energy / c2)

	@property
	def gamma(self) -> None:
		return

	@gamma.setter
	def gamma(self) -> Exception:
		raise SyntaxError("Can\'t directly set the gamma of a Body.")

	@gamma.getter
	def gamma(self) -> Scalar:
		return 1 / sqrt(1 - ((abs(self.velocity) ** 2) / c2))

# Body implementations

class Particle(Body):
	def atoms(self) -> Iterable[Atom]:
		return [Atom(
			parent = self,
			location = self.location,
			energy = self.restEnergy,
			**self.properties
		)]

class RelativisticParticle(Body):
	def atoms(self) -> Iterable[Atom]:
		return [Atom(
			parent = self,
			location = self.location,
			energy = self.restEnergy * self.gamma,
			**self.properties
		)]

class Shell(Body):

	# Requires a "radius" and "density" argument

	def atoms(self) -> Iterable[Atom]:
		points = []
		phi = pi * (3 - sqrt(5))

		for i in range(self.density):
			y = 1 - (i / float(self.density - 1)) * 2
			radius = sqrt(1 - (y ** 2)) * self.radius
			theta = phi * i

			x = cos(theta) * radius
			z = sin(theta) * radius

			points.append(Vector(x, y, z))

		return [
			Atom(
				parent = self,
				location = location,
				energy = self.restEnergy / self.density,
				**self.properties
			) for location in points
		]

class RelativisticShell(Body):
	def atoms(self) -> Iterable[Atom]:
		points = []
		phi = pi * (3 - sqrt(5))

		for i in range(self.density):
			y = 1 - (i / float(self.density - 1)) * 2
			radius = sqrt(1 - (y ** 2)) * self.radius
			theta = phi * i

			x = cos(theta) * radius
			z = sin(theta) * radius

			points.append(Vector(x, y, z))

		return [
			Atom(
				parent = self,
				location = location,
				energy = self.restEnergy / self.density,
				**self.properties
			) for location in points
		]

class Field(ABC):

	"""
	Generalized Python representation of a force field, i.e.
	the electromagnetic field which is a field of virtual photons,
	the color charge field which is a field of virtual gluons,
	and the weak field which is a field of virtual W and Z bosons.

	The Field.couple(a, b) function is used to return the forces applied
	to particles a and b, respectively.
	"""

	IGNORE = "ignore"
	WARN = "warn"
	ERROR = "error"

	couplingProperties: list[str]
	decoupledBehavior: str = IGNORE

	def __init__(self, resolution: int=1000, **kwargs) -> None:
		self.calculus = ExtendedCalculus(resolution)
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])

	def couples(self, atom: Atom) -> bool:
		for prop in self.couplingProperties:
			if prop not in atom.properties:
				return False
		return True

	@abstractmethod
	def potential(self, st: "Spacetime", location: Vector) -> tuple[Vector, Vector]:
		raise NotImplementedError

	def couple(self, st: "Spacetime", atom: Atom) -> tuple[Vector, Vector]:
		if self.couples(atom):
			return -1 * self.calculus.gradient(lambda v: self.potential(st, v), atom.location) * atom.energy // c2
		else:
			if self.decoupledBehavior == self.IGNORE:
				return Vector(0, 0, 0), Vector(0, 0, 0)
			elif self.decoupledBehavior == self.WARN:
				print("Warning: at least one particle is decoupled from the " + type(self).__name__ + " field.")
			elif self.decoupledBehavior == self.ERROR:
				raise RuntimeError("Bad coupling.")
			else:
				raise SyntaxError("Bad coupling behavior set.")

class Metric(ABC):
	PMMM = "+---"
	MPPP = "-+++"
	_SIGNATURES = [PMMM, MPPP]

	def __init__(self, resolution: int) -> None:
		self._signature = self.MPPP
		self._spacetime: "Spacetime" = None
		self.calculus = ExtendedCalculus(resolution)

	def __repr__(self) -> str:
		return "<" + type(self).__name__ + " metric, resolution " + str(self.calculus.resolution) + ">"
	
	@property
	def signature(self):
		return self._signature
		
	@signature.setter
	def signature(self, value: str) -> None:
		if value not in self.signatures:
			raise NameError("Bad metric signature" + repr(value) + ".")
		self._signature = value
		
	@signature.getter
	def signature(self) -> str:
		return self._signature
		
	@abstractmethod
	def space(self, location: Vector) -> Scalar:
		raise NotImplementedError
		
	def spaceInterval(self, a: Vector, b: Vector) -> Scalar:
		return self.calculus.integrateLineSegment(self.space, a, b)
		
	@abstractmethod
	def time(self, location: Vector) -> Scalar:
		raise NotImplementedError
		
	def timeInterval(self, a: Vector, b: Vector) -> Scalar:
		return self.calculus.integrateLineSegment(self.time, a, b)
		
	def spacetimeInterval(self, a: Vector, b: Vector) -> Scalar:
		if self.signature == self.PMMM:
			return self.timeInterval(a, b) - self.spaceInterval(a, b)
		elif self.signature == self.MPPP:
			return self.spaceInterval(a, b) - self.timeInterval(a, b)
		else:
			raise SyntaxError("Bad metric signature.")
			
	# Equipment methods
	@property
	def spacetime(self):
		return self._spacetime

	@spacetime.setter
	def spacetime(self, value: "Spacetime") -> None:
		self._spacetime = value
		if value != None:
			self._spacetime._metric = self
			
	@spacetime.getter
	def spacetime(self) -> "Spacetime":
		return self._spacetime

class Spacetime:
	def __init__(self) -> None:
		self.fields = []
		self._metric: Metric = None
		self._bodies = {}

	def __iter__(self) -> Iterable[Body]:
		return iter(self.bodies)

	def __getitem__(self, id: str) -> Body:
		return self._bodies[id]

	def __contains__(self, item) -> bool:
		if type(item) == str:
			return item in self._bodies.keys()
		
		if issubclass(type(item), Force):
			for field in self.fields:
				if type(field) == item or field == item:
					return True
			return False

		return type(self.metric) == item or self.metric == item

	# === Simulation properties === #

	# Metric

	@property
	def metric(self) -> None:
		return self._metric
		
	@metric.setter
	def metric(self, value: Metric) -> None:
		self._metric = value
		if value != None:
			self._metric._spacetime = self
		else:
			if self._metric != None:
				self._metric._spacetime = None
			
	@metric.getter
	def metric(self) -> Metric:
		return self._metric

	# Bodies

	@property
	def bodies(self) -> None:
		return self._bodies 

	@bodies.setter
	def bodies(self, value: Any) -> Exception:
		raise SyntaxError("Can\'t directly set the Spacetime.bodies attribute.")

	@bodies.getter
	def bodies(self) -> Iterable[Body]:
		return list(self._bodies.values())
	
	def addBody(self, **bodies: dict[str, Body]) -> None:
		for bodyID, body in zip(bodies.keys(), bodies.values()):
			body.id = bodyID
			self._bodies[body.id] = body

	def removeBody(self, *bodyIDs: tuple[str]) -> None:
		for bodyID in bodyIDs:
			if bodyID in self:
				del self._bodies[bodyID]

	# Atoms, really a component of Bodies

	@property
	def atoms(self) -> None:
		return

	@atoms.setter
	def atoms(self, value: Any) -> Exception:
		raise SyntaxError("Can\'t directly set the Spacetime.atoms attribute.")

	@atoms.getter
	def atoms(self) -> Iterable[Atom]:
		atoms = []
		for body in self.bodies:
			for atom in body.atoms():
				if atom.parent != body:
					atom.parent = body
				atoms.append(atom)

	# Fields

	def addField(self, *fields: tuple[Field]) -> None:
		if field in self:
			raise NameError("Spacetime already connected to a " + type(field).__name__ + " field.")

		for field in fields:
			self.fields.append(field)

	def removeField(self, *fields: tuple[Field]) -> None:
		for f in fields:
			for index, field in enumerate(self.fields):
				if type(field).__name__ == type(f).__name__:
					self.fields.pop(index) # no, that won't mess anything up
					# we're iterating over an enumerate() object, not the list
					# itself, don't worry
					break