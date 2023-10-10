from abc import ABC
from abc import abstractmethod

from kolibri.utils import *

class Field(ABC):
	
	def __init__(self, **kwargs: dict[str, Any]) -> None:
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])

		self.spacetime: "Spacetime" = None

	@abstractmethod
	def potential(self, location: Vector) -> Scalar:
		pass
