from kolibri.utils import *
from kolibri.constants import *
from kolibri.entity import *

class Force(ABC):
	
	"""
	Force field/interaction base class.
	Should not be used.
	"""

	def __init__(self, **variables: dict[str, Scalar]) -> None:
		for key in variables.keys():
			setattr(self, key, variables[key])

		self._spacetime: "Spacetime" = None

	@property
	def spacetime(self) -> None:
		"""
		Spacetime property.
		"""

		return
	
	@spacetime.getter
	def spacetime(self) -> Union[None, "Spacetime"]:
		return self._spacetime

	@spacetime.setter
	def spacetime(self, spacetime: "Spacetime") -> None:
		"""
		Set the spacetime of the force.
		Equivalent to adding the force to the spacetime.
		"""

		self._spacetime = spacetime
		if spacetime is not None:
			self._spacetime._metric = self # probably won't cause issues

	@abstractmethod
	def atomicForce(self, atom: Atom) -> Vec3:
		pass
	
	@abstractmethod
	def coupling(self, atom: Atom) -> Scalar:
		pass
	
	def entityForce(self, entity: Entity) -> tuple[Vec3, Vec3]:
		"""
		Calculate the force acting on an entity (and the
		offset at which that force is applied).
		"""

		com, atoms = entity.centerOfMass(giveAtoms=True)

		fs: list[Vec3] = []
		locs: list[Vec3] = []

		for atom in atoms:
			fs.append(self.atomicForce(atom))
			locs.append(atom.location)

		fnet = Vector.zero(3)
		for f in fs:
			fnet += f

		if entity.POINT:
			return (fnet, com)

		location = Vector.zero(3)
		for index, loc in enumerate(locs):
			location += loc * abs(f[index])
		location /= sum([abs(f) for f in fs])

		return fnet, location
	
class Field(Force):

	"""
	The Field is given as a gradient of a potential
	rather than discrete interactions.
	"""

	h: Scalar = 0.000001

	def __post_init__(self) -> None:
		self.calculus = Calculus(h)

	@abstractmethod
	def potential(self, atom: Atom, location: Vec3) -> Scalar:
		pass
	
	def V(self, atom: Atom) -> Callable[[Vec3], Scalar]:
		def potential(location):
			return self.potential(atom, location)
		return potential
	
	def atomicForce(self, atom: Atom) -> Vec3:
		return -1 * self.calculus.gradient(self.V(atom), atom.location) * self.coupling(atom)
	
class Interaction(Force):

	"""
	The Interaction is given as a sum of discrete
	interparticle interactions rather than a continuous
	field.
	"""

	@abstractmethod
	def interact(self, a: Atom, b: Atom) -> Scalar:
		pass

	def atomicForce(self, atom: Atom) -> Vec3:
		f = Vector.zero(3)
		for otherAtom in self.spacetime.otherAtoms(atom):
			dr = (otherAtom.location - atom.location).normal()
			f += dr * self.interact(self, otherAtom)
		return f