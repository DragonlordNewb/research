from abc import ABC
from abc import abstractmethod

from kolibri.utils import *

class Metric(ABC):

	def __init__(self, **kwargs: dict[str, Any]) -> None:
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])

		self.spacetime: "Spacetime" = None

	def __repr__(self) -> str:
		return "<" + type(self).__name__ + " metric>"

	@abstractmethod
	def timewarp(self, location: Vector) -> Scalar:
		pass
	
	@abstractmethod
	def spacewarp(self, location: Vector) -> Scalar:
		pass
	
	def warps(self, location: Vector) -> tuple[Scalar, Scalar]:
		return self.timewarp(location), self.spacewarp(location)