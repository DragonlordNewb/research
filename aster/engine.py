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

	@staticmethod
	def register(*names: tuple[str]) -> Callable[[type], type]:
		def deco(cls):
			cls.names = []
			for name in names:
				Body.BODIES[name] = cls
				cls.names.append(name)
			return cls
		return deco

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
	def register(*names: tuple[str]) -> Callable[[type], type]:
		def deco(cls):
			cls.names = []
			for name in names:
				Metric.METRICS[name] = cls
				cls.names.append(name)
			return cls
		return deco

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
	def act(self, a: Atom, b: Atom) -> tuple[Vector, Vector]:
		pass

	@staticmethod
	def register(*names: tuple[str]) -> Callable[[type], type]:
		def deco(cls) -> type:
			cls.names = []
			for name in names:
				Force.FORCES[name] = cls
				cls.names.append(name)
			return cls
		return deco

	@classmethod
	def lookup(cls, name: str) -> type:
		return cls.FORCES[name]

	def data(self) -> bytes:
		forceName = ""
		for name in self.names:
			if forceName == "" or len(name) < len(forceName):
				forceName = name
		forceName = forceName.encode("utf-8")
		if len(forceName) < 32:
			forceName += bytes(32 - len(forceName))

		return forceName + pack("!d", self.coupling)

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

	def render(self, body: Body) -> bytes:
		self.bodies.append(body)
		id = randbytes(32)
		self.bodies[-1].id = id
		return id

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

	# static info storage

	@cache
	def header(self) -> bytes:
		magic = b"ASTERSDF"

		if self.metric != None:
			if not hasattr(self.metric, "names"):
				raise SyntaxError("Currently-equipped Metric (" + type(self.metric).__name__ + ") was not properly registered with a name.")
			metricName = ""
			for name in self.metric.names:
				if metricName == "" or len(name) < len(metricName):
					metricName = name
			if metricName == "":
				raise SyntaxError("Currently-equipped Metric (" + type(self.metric).__name__ + ") was not properly registered with a name.")
			if len(metricName) > 32:
				raise SyntaxError("Currently-equipped Metric (" + type(self.metric).__name__ + ") did not have a sufficiently-short name registered.")

			metricName = metricName.encode("utf-8")
			if len(metricName) < 32:
				metricName += bytes(32 - len(metricName))

		else:
			metricName = bytes(32)

		resolution = pack("!Q", self.resolution)

		delimiter = b"THE-WORLD-IS-IN-YOUR-HANDS\x00\x00\x00\x00\x00\x00"

		return magic + metricName + resolution + delimiter

	def data(self) -> bytes:
		pass
