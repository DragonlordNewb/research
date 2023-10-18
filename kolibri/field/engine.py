from kolibri.utils import *

class Field(ABC):

	REGISTRATIONS = {}

	@classmethod
	def register(cls, name: str) -> type:
		def deco(ncls):
			cls.REGISTRATIONS[name.lower()] = ncls
			return ncls
		return deco

	@classmethod
	def lookup(cls, name: str) -> type:
		return cls.REGISTRATIONS[name.lower()]

	signature: set[str]
	
	def __init__(self, h: Scalar=0.000001, **kwargs: dict[str, Any]) -> None:
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])

		self.spacetime: "Spacetime" = None
		self.calculus = Calculus(h)

	@abstractmethod
	def potential(self, location: Vector) -> Scalar:
		pass