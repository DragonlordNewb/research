from kolibri.body import Body
from kolibri.body import Atom
from kolibri.utils import *

class Particle(Body):
	def atoms(self) -> Iterable[Atom]:
		return Atom(self.locationm, **self.charges)