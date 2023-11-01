"""
Module for base classes for forces and interactions.

Note that, strictly speaking, any interaction can be 
modelled as a force and any force can be modelled as an
interaction. The two different base classes just differ
in how they calculate the force on a particle. Otherwise
they're identical and can be used interchangeably.
"""

from kolibri.utils import *
from kolibri.constants import *
from kolibri.entity import *

class Force(ABC):
	
	"""
	Force field/interaction base class.
	Should not be used.
	"""

	# Registration stuff

	REGISTRATIONS = {}
	@classmethod
	def register(cls, name: str) -> Callable[[type], type]:
		def deco(ncls):
			cls.REGISTRATIONS[name.lower()] = ncls
			return ncls
		return deco
	@classmethod
	def getType(cls, name: str) -> type:
		return cls.REGISTRATIONS[name.lower()]

	# Actual stuff

	def __init__(self, **variables: dict[str, Scalar]) -> None:
		for key in variables.keys():
			setattr(self, key, variables[key])

		self._spacetime: "Spacetime" = None

		self.__post_init__()

	def __post_init__(self) -> None:
		self.calculus = Calculus(h)

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

	@abstractmethod
	def potential(self, atom: Atom, location: Vec3) -> Scalar:
		pass

	@abstractmethod
	def coupling(self, atom: Atom) -> Scalar:
		pass
	
	def V(self, atom: Atom) -> Callable[[Vec3], Scalar]:
		def potential(location):
			return self.potential(atom, location)
		return potential
	
	def atomicForce(self, atom: Atom) -> Vec3:
		grad = self.calculus.gradient(self.V(atom), atom.location)
		coupling = self.coupling(atom)
		return -coupling * grad
	
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
			interaction = self.interact(atom, otherAtom)
			f += dr * interaction
		return f
	
# ===== Implementations ===== #

@Force.register("ElectromagneticF")
class ElectromagneticField(Field):
	"""
	Electromagnetic field!
	"""

	def potential(self, atom, location):
		p = 0
		for otherAtom in self.spacetime.otherAtoms(atom):
			if "electric" not in otherAtom.charges.keys():
				continue
			p += ke * otherAtom.charges["electric"] / abs(otherAtom.location - location)
		return p
	
	def coupling(self, atom: Atom):
		if "electric" not in atom.charges.keys():
			return 0
		return atom.charges["electric"]
	
@Force.register("ElectromagneticI")
class ElectromagneticInteraction(Interaction):

	"""
	Electromagnetic interaction!
	"""

	def interact(self, a, b):
		if not ("electric" in a.charges.keys() and "electric" in b.charges.keys()):
			return 0
		return -(b.charges["electric"] * ke) * sgn(a.charges["electric"]) / self.spacetime.metric.distance(a, a.location, b.location)
	
	def coupling(self, atom):
		if "electric" not in atom.charges.keys():
			return 0
		return atom.charges["electric"]
	
@Force.register("GravitationalI")
class GravitationalInteraction(Interaction):

	"""
	Gravitational interaction!
	"""

	def interact(self, a, b):
		pass