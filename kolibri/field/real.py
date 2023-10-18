from kolibri.field.engine import Field
from kolibri.utils import *

@Field.register("potentialwell")
class PotentialWell(Field):

	signature = set()

	radius: Scalar = 1
	depth: int = 2
	power: Scalar = 0.00001

	def potential(self, location: Vector) -> None:
		return abs(Vector(
			(location.x / self.radius) ** self.depth,
			(location.y / self.radius) ** self.depth,
			(location.z / self.radius) ** self.depth
		) * self.power)