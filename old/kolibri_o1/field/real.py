from kolibri.field.engine import Field
from kolibri.body.engine import Atom
from kolibri import constants
from kolibri.utils import *

@Field.register("well")
class Well(Field):

	signature = set()

	radius: Scalar = 2
	depth: int = 10

	def coupling(self, atom: Atom) -> int:
		return 1

	def potential(self, spacetime: "Spacetime", location: Vector) -> Scalar:
		return (abs(location) / self.radius) ** self.depth
