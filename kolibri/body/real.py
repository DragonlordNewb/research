from kolibri.body.engine import Body
from kolibri.body.engine import Atom
from kolibri.utils import *

@Body.register("particle")
class Particle(Body):
	def atoms(self) -> Iterable[Atom]:
		return [self.makeAtom(self.location, **self.charges)]