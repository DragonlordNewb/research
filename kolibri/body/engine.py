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

	CANNOT_SET_EXPERIENCED_CLASS = SystemFailure(SystemFailure.FATAL, "Cannot directly set experienced class.", "Cannot directly set the experienced class on a ClassificationTracker object.")
	CANNOT_SET_PROPER_CLASS = SystemFailure(SystemFailure.FATAL, "Cannot directly set proper class.", "Cannot directly set the proper class on a ClassificationTracker object.")

	def __init__(self):
		self.experiencedTime = 0
		self.experiencedSpace = 0
		self.properTime = 0
		self.properSpace = 0

	@staticmethod
	def classify(v: Scalar) -> None:
		if v < c:
			return self.BRADYONIC
		if v == c:
			return self.LUXONIC
		if v > c:
			return self.TACHYONIC

	@property
	def experienced(self) -> None:
		return
	
	@experienced.setter
	def experienced(self, value: Any) -> Exception:
		self.CANNOT_SET_EXPERIENCED_CLASS.panic()

	@experienced.getter
	def experienced(self) -> str:
		return self.classify(self.experiencedSpace / self.experiencedTime)

	@property
	def proper(self) -> None:
		return
	
	@proper.setter
	def proper(self, value: Any) -> Exception:
		self.CANNOT_SET_PROPER_CLASS.panic()

	@proper.getter
	def proper(self) -> str:
		return self.classify(self.properSpace / self.properTime)

	def reset(self) -> None:
		self.experiencedTime = self.experiencedSpace = self.properTime = self.properSpace = 0

class Body(ABC):
	def __init__(self, id: str, location: Vector, **charges: dict[str, Any]) -> None:
		self.id = id

		self.location = location
		self.velocity = Vector.zero()

		for key in charges.keys():
			setattr(self, key, charges[key])

		self.signature = set(charges.keys())

		self.charges = charges

		self.classif = ClassificationTracker()

		self.spacetime: "Spacetime" = None

	def __repr__(self) -> str:
		return "<" + type(self).__name__ + " body at " + repr(self.location) + ">"

	@abstractmethod
	def atoms(self) -> Iterable[Atom]:
		pass
	
	def displace(self, displacement: Vector) -> None:
		self.location += displacement

	def move(self, location: Vector) -> None:
		self.location = location
	
	def accelerate(self, acceleration: Vector) -> None:
		self.velocity += acceleration

	def aim(self, velocity: Vector) -> None:
		self.velocity = velocity

	def tick(self, resolution: Scalar) -> None:
		properTime = resolution
		properSpace = self.velocity * resolution

		timewarp, spacewarp = self.spacetime.metric.warps(self.location)

		experiencedTime = properTime * timewarp
		experiencedSpace = self.velocity * (resolution * timewarp) * spacewarp

		self.classif.properTime += properTime
		self.classif.properSpace += abs(properSpace)
		self.classif.experiencedTime += experiencedTime
		self.classif.experiencedSpace += abs(experiencedSpace)

		self.location += experiencedSpace