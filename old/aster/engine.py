# Advanced SpaceTime Engineering Research software simulation engine.
# This section of the software creates the appropriate simulations of
# real spacetime and its behavior under various metrics.

# Lux Bodell, 2023.
# This code is licensed under the Creative Commons BY-NC-ND license.
# That means that you can use the code and learn from it, but you
# can't sell it or prepare derivative works.

from aster.core import Vector
from aster.core import Scalar
from aster.core import Integrator

from abc import ABC
from abc import abstractmethod

from functools import cache

from struct import pack
from struct import unpack

from typing import Iterable
from typing import Union
from typing import Any
from typing import Callable

from time import time as computerClock # as to avoid ambiguity

from random import randbytes

class Atom:

	"""
	The Atom class is an abstract object representing an infinitesimal portion of
	a larger object.

	The Body class represents the object itself, and has a method which returns a
	list of the Atoms that the Body contains.
	"""

	def __init__(self, energy: Scalar, charge: Scalar, location: Vector) -> None:
		self.energy = energy
		self.location = location
		self.charge = charge

	def __repr__(self) -> str:
		return "<Atom: " + repr(self.energy) + " at " + repr(self.location) + ">"

	def __iter__(self) -> Iterable[Union[Scalar, Vector]]:
		return iter((self.energy, self.location))

class Body(ABC):

	"""
	The Body class represents a physical object in the most accurate way possible.
	The class must be subclassed to provide the Body.atoms() function, which takes
	in the attributes of the Body subclass's instance and returns a list of Atoms,
	including the Atoms' coordinates, charge, energy, etc.
	"""

	BODIES = {}

	def __init__(self, restEnergy: Scalar, **kwargs: dict[str, Any]) -> None:
		self.restEnergy = restEnergy

		self.location = Vector(0, 0, 0)
		self.angle = Vector(0, 0, 0)
		self.velocity = Vector(0, 0, 0)
		self.rotation = Vector(0, 0, 0)

		self.experiencedTime = 0
		self.experiencedSpace = 0

		self.id = None

		for key in kwargs.keys():
			setattr(self, key, kwargs[key])

	def __iter__(self) -> Iterable[Atom]:
		return iter(self.atoms())

	def __eq__(self, other: "Body") -> bool:
		return self.id == other.id

	@abstractmethod
	def atoms(self) -> list[Atom]:
		pass

	def centerOfMass(self) -> Vector:
		locations = [atom.location for atom in self.atoms()]
		sum = Vector(0, 0, 0)
		for location in locations:
			sum += location
		return sum / len(locations)

	@staticmethod
	def register(cls) -> type:
		Body.BODIES[cls.__name__] = cls
		return cls

	@classmethod
	def lookup(cls, name: str) -> type:
		return cls.BODIES[name]

class Metric(ABC):

	"""
	The Metric is an abstract object which must be subclassed.
	It provides a way to dictate the passage of time and behavior of spacetime
	at given points.
	"""

	METRICS = {}

	def __init__(self, resolution: int=1000) -> None:
		self.spacetime: "Spacetime" = None
		self.integrator = Integrator(resolution)

	def __repr__(self) -> str:
		return "<" + self.__name__ + " metric of resolution " + str(self.integrator.resolution) + ">"

	def equip(self, spacetime: "Spacetime", force: bool=False) -> None:
		if type(spacetime) == Spacetime:
			if spacetime.metric != None:
				if not force:
					raise RuntimeError("Spacetime is already equipped with a Metric.")
			self.spacetime = spacetime
			spacetime.metric = self
			return
		raise TypeError("Can only equip a Metric to a Spacetime object instance.")

	def unequip(self) -> None:
		self.spacetime.metric = None
		self.spacetime = None

	@abstractmethod
	def spaceContraction(self, location: Vector) -> Scalar:
		pass

	@abstractmethod
	def timeDilation(self, location: Vector) -> Scalar:
		pass

	def distance(self, a: Vector, b: Vector) -> Scalar:
		return self.integrator.trivariate(self.spaceContraction, a, b)

	@staticmethod
	def register(cls) -> type:
		Metric.METRICS[cls.__name__] = cls

	@classmethod
	def lookup(cls, name: str) -> type:
		return cls.METRICS[name]

class Force(ABC):

	"""
	The Force class is also highly abstract, representing a 'force' that can act
	on Bodys. The Force.act(a, b) function must be overridden to take in two Atoms
	and return a tuple of the respective accelerations that are applied to each of them.

	The Force also accepts keyword arguments, so that the physical parameters of the
	force (i.e. G, c, mu-0, epsilon-0, etc.) can be altered to manipulate the simulation
	at a deeper level.
	"""

	FORCES = {}

	def __init__(self, coupling: Scalar=1) -> None:
		self.coupling = coupling

	def __eq__(self, other: "Force") -> bool:
		if type(self) == type(other):
			return self.coupling == other.coupling
		return False

	@abstractmethod
	def act(self, a: Atom, b: Atom, distance: Scalar) -> tuple[Vector, Vector]:
		pass

	@staticmethod
	def register(cls) -> type:
		Force.FORCES[cls.__name__] = cls

	@classmethod
	def lookup(cls, name: str) -> type:
		return cls.FORCES[name]

class Spacetime:

	"""
	The Spacetime is the 'god' class of the module. It provides a unified mechanism by which
	Metrics, Forces, and Bodys can be meddled and experimented with.

	Metrics are Spacetime.equip(metric)'d, Forces are Spacetime.apply(force)'d, and Bodies
	are Spacetime.render(body)'d.

	The simulation is ticked forward in variable-resolution "epochs". Spacetime.advance(n)
	ticks the simulation forward n epochs; Spacetime.advanceComputerSeconds(n) advances the
	simulation by n seconds, so that n seconds will have passed inside the simulation (probably
	far fewer in the real world); Spacetime.advanceRealSeconds(n) advances the simulation
	continuously until n seconds have passed.
	"""

	def __init__(self, resolution: int) -> None:
		self.metric: Metric = None
		self.bodies = []
		self.forces = []
		self.resolution = resolution

	def __repr__(self) -> str:
		if self.metric == None:
			return "<Spacetime of unknown metric and " + str(len(self.bodies)) + " bodies>"
		if len(self.bodies) == 1:
			objs = " body>"
		else:
			objs = " bodies>"
		return "<" + type(self.metric).__name__ + " Spacetime of " + str(len(self.bodies)) + objs

	# configuration methods

	def equip(self, metric: Metric, force: bool=False) -> None:
		if issubclass(type(metric), Metric):
			if metric.spacetime != None:
				if not force:
					raise RuntimeError("Metric is already equipped by another Spacetime.")
			self.metric = metric
			metric.spacetime = self
			return
		raise TypeError("Can only equip a Spacetime with a Metric object instance.")

	def unequip(self) -> None:
		self.metric.spacetime = None
		self.metric = None

	def apply(self, force: Force) -> None:
		for f in self.forces:
			if type(force) == type(f):
				return
		self.forces.append(force)

	def cancel(self, force: Force) -> None:
		i = -1
		for f in self.forces:
			i += 1
			if f == force:
				self.forces.pop(i)
				return

	def render(self, body: Body, customID=None) -> bytes:
		self.bodies.append(body)
		id = randbytes(32)
		self.bodies[-1].id = id
		if customID:
			self.bodies[-1].id = customID
		return id

	def getBody(self, id) -> Body:
		for body in self.bodies:
			if body.id == id:
				return body
		raise NameError("No such body.")

	def derender(self, id: bytes) -> Body:
		i = -1
		for body in self.bodies:
			i += 1
			if body.id == id:
				result = self.bodies.pop(i)
				result.id = None
				return result
		return NameError("No such body.") # don't raise it, generally just doesn't matter that much

	# functional methods

	def distance(self, a: Vector, b: Vector) -> Scalar:
		return self.metric.distance(a, b)

	# ticking

	def advance(self, n) -> None:
		if n != 1:
			for _ in range(n - 1):
				self.advance(1)

		for body1 in self.bodies:
			for body2 in self.bodies:
				if body1 == body2:
					continue

				vi1 = body1.velocity
				vi2 = body2.velocity

				force1 = Vector(0, 0, 0)
				torque1 = Vector(0, 0, 0)
				force2 = Vector(0, 0, 0)
				torque2 = Vector(0, 0, 0)

				center1 = body1.centerOfMass()
				center2 = body2.centerOfMass()

				for atom1 in body1.atoms():
					for atom2 in body2.atoms():
						for force in self.forces:
							distance = self.metric.distance(atom1.location, atom2.location)
							f1, f2 = force.act(atom1, atom2, distance)
							force1 += f1 * self.metric.timeDilation(atom1.location)
							force2 += f2 * self.metric.timeDilation(atom2.location)

							r1, r2 = atom1.location - center1, atom2.location - center2
							t1, t2 = Vector.cross(r1, f1), Vector.cross(r2, f2)
							torque1 += t1 * self.metric.timeDilation(atom1.location)
							torque2 += t2 * self.metric.timeDilation(atom2.location)

				body1.velocity += force1 / self.resolution
				body2.velocity += force2 / self.resolution
				body1.rotation += torque1 / self.resolution
				body2.rotation += torque2 / self.resolution
				body1.location += body1.velocity / self.resolution
				body2.location += body2.velocity / self.resolution
				body1.angle += body1.rotation / self.resolution
				body2.angle == body2.rotation / self.resolution

				vf1 = body1.velocity
				vf2 = body2.velocity

				dS1 = abs(vf1 - vi1)
				dS2 = abs(vf2 - vi2)

				time1 = []
				time2 = []
				space1 = []
				space2 = []

				for atom in body1.atoms():
					time1.append(self.metric.timeDilation(atom.location))
					space1.append(self.metric.spaceContraction(atom.location) * dS1)
				for atom in body2.atoms():
					time2.append(self.metric.timeDilation(atom.location))
					space2.append(self.metric.spaceContraction(atom.location) * dS2)

				experiencedTime1 = sum(time1) / len(time1)
				experiencedTime2 = sum(time2) / len(time2)
				experiencedSpace1 = sum(space1) / len(space1)
				experiencedSpace2 = sum(space2) / len(space2)

				body1.experiencedTime += experiencedTime1 / self.resolution
				body2.experiencedTime += experiencedTime2 / self.resolution
				body1.experiencedSpace += experiencedSpace1 / self.resolution
				body2.experiencedSpace += experiencedSpace2 / self.resolution

		return

	def advanceComputerSeconds(self, n: Scalar) -> None:
		ticks = self.resolution * n
		self.advance(ticks)

		return

	def advanceRealSeconds(self, n: Scalar, batchSize: int=None) -> None:
		if batchSize == None:
			batchSize = self.resolution

		et = computerClock() + n
		while computerClock() < n:
			self.advance(batchSize)

		return
