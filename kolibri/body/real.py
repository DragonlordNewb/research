from kolibri.body.engine import Body
from kolibri.body.engine import Atom
from kolibri.utils import *

class Particle(Body):
	def atoms(self) -> Iterable[Atom]:
		return [Atom(self.location, **self.charges)]