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

from typing import Iterable
from typing import Union
from typing import Any

class Atom:
	def __init__(self, energy: Scalar, location: Vector) -> None:
		self.energy = energy
		self.location = location

	def __repr__(self) -> str:
		return "<Atom: " + repr(self.energy) + " at " + repr(self.location) + ">"

	def __iter__(self) -> Iterable[Union[Scalar, Vector]]:
		return iter((self.energy, self.location))

class Body(ABC):
	def __init__(self, restEnergy: Scalar, **kwargs: dict[str, Any]) -> None:
		self._energy = energy
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])

		self._location = Vector(0, 0, 0)
		self._angle = Vector(0, 0, 0)
		self._velocity = Vector(0, 0, 0)
		self._rotation = Vector(0, 0, 0)

	def __iter__(self) -> Iterable[Atom]:
		return iter(self.atoms())

	@abstractmethod
	def atoms(self) -> list[Atom]:
		pass

	# angle and rotational properties

class Metric(ABC):
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
		return self.integrator.fieldLineIntegral(self.spaceContraction, a, b)

class Spacetime:
	def __init__(self) -> None:
		self.metric: Metric = None
		self.bodies = []

	def __repr__(self) -> str:
		if self.metric == None:
			return "<Spacetime of unknown metric and " + str(len(self.objects)) + " objects>"
		if len(self.objects) == 1:
			objs = " body>"
		else:
			objs = " bodies>"
		return "<" + type(self.metric).__name__ + " Spacetime of " + str(len(self.objects)) + objs

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
