from abc import ABC
from abc import abstractmethod

from kolibri.utils import *

class Field(ABC):
	
	def __init__(self, **kwargs: dict[str, Any]) -> None:
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])

		self._spacetime: "Spacetime" = None

	@property
	def spacetime(self) -> None:
		return

	@spacetime.setter
	def spacetime(self, value: "Spacetime") -> None:
		if value == None and self._spacetime != None:
			self._spacetime.field
		self._spacetime = value
		
