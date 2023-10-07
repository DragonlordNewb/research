from abc import abstractmethod
from abc import ABC

from kolibri.utils import *
from kolibri.constants import *

class Atom:
	def __init__(self, location: Vector, **charges: dict[str, Any]) -> None:
		self.location = location

		for key in charges.keys():
			setattr(self, key, charges[key])

		self.signature = set(charges.keys())

class ClassificationTracker:

	BRADYONIC = "bradyonic"
	LUXONIC = "luxonic"
	TACHYONIC = "tachyonic"

	def __init__(self):
		self.experiencedTime = 0
		self.experiencedSpace = 0
		self.properTime = 0
		self.properSpace = 0

	def experiential(self) -> str:
		return self.BRADYONIC if self.experiencedSpace / self.experiencedTime < c

class Body(ABC):
	def __init__(self, id: str, location: vector, **charges: dict[str, Any]) -> None:
		self.id = id

		self.location = location
		self.velocity = Vector.zero()

		for key in charges.keys():
			setattr(self, key, charges[key])

		self.signature = set(charges.keys())

		self.classif.

	@abstractmethod
	def atoms(self) -> Iterable[Atom]:
		pass
