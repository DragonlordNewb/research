from abc import abstractmethod
from abc import ABC

from kolibri.utils import *

class Atom:
	def __init__(self, location: Vector, **charges: dict[str, Any]) -> None:
		self.location = location

		for key in charges.keys():
			setattr(self, key, charges[key])

		self.signature = set(charges.keys())

class Body(ABC):
	def __init__(self, location: vector, **charges: dict[str, Any]) -> None:
		self.location = location
		self.velocity = Vector.zero()

		for key in charges.keys():
			setattr(self, key, charges[key])

		self.signature = set(charges.keys())

	@abstractmethod
	def atoms(self) -> Iterable[Atom]:
		pass