from kolibri.field.engine import Field
from kolibri.body.engine import Atom
from kolibri import constants
from kolibri.utils import *

@Field.register("gravitational")
class GravitationalField(Field):
	
	G: Scalar = constants.G
	
	def potential(self, spacetime: "Spacetime", atom: Atom) -> Callable[[Vector], Scalar]:
		v = 0
		for body, atom in spacetime.atoms():
			if body == atom.parent:
				continue
			v += G * atom.mass / 