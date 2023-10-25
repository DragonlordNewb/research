from kolibri.constants import *
from kolibri.utils import *

# There are two types of forces: the Interaction
# and the Field.
#
# Interactions exert forces between only interacting
# particles by calculating the exerted force between
# all n^2 - n pairs of interacting particles.
#
# Fields exert forces between only coupled particles
# by calculating the field potential at the location
# of each of the n particles and using a gradient to
# determine the direction and magnitude of the force.

class Force(ABC):

	"""
	The Force is an abstract base class for the
	Interaction and the Field classes exclusively.
	Do not use.
	"""

	def __init__(self, **parameters) -> None:
		for key in parameters.keys():
			setattr(self, key, parameters[key])

		self.spacetime: "Spacetime" = None

	@abstractmethod
	def apply(self, atom: "Atom") -> tuple[Vector, Vector]:
		"""
		Return a tuple of a Vector representing the force
		vector and a Vector representing the location at
		which that force is applied (potentially torquing
		the atom).
		"""

		pass

class Field(Force):

	signature: set[str]
	h: Scalar = Decimal(0.000001)
	
	def __post_init__(self) -> None:
		self.calculus = Calculus(self.h)

	@abstractmethod
	def potential(self, atom: "Atom") -> None:
		pass
	
	@abstractmethod
	def coupling(self, atom: "Atom") -> Scalar:
		pass
	
	def apply(self, atom: "Atom") -> tuple[Vector, Vector]:
		return -self.calculus.gradient(self.potential) * self.coupling(atom)