from kolibri.utils import *
from kolibri.constants import *

from dataclasses import dataclass

@dataclass
class Atom:
	
	parent: "Entity"
	id: str
	location: Vec3
	mass: Scalar
	charges: dict[str, Scalar]

	def __eq__(self, other: "Atom"):
		if type(self) != type(other):
			return False
		return self.id == other.id

class Entity(ABC):

	"""
	Entity is the class that represents the 
	physical objects embedded in spacetime.
	Can be given arbitrary properties, plus
	a function Entity.atoms() that returns
	a list of atoms that represent the object
	as a whole.
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

	POINT: bool

	def __init__(self, name: str, location: Vec3, restMass: Scalar, **charges: dict[str, Scalar]) -> None:
		self.name = name
		self.location = location
		self.angle = Vector.zero(3)
		self.velocity = Vector.zero(3)
		self.spin = Vector.zero(3)

		self.restMass = Decimal(restMass)
		self.charges = charges

	@abstractmethod
	def atoms(self) -> list[Atom]:
		pass
	
	# Useful functions for physical values

	def centerOfMass(self, giveAtoms: bool=False) -> Vec3:
		"""
		Simple center-of-mass.

		The function can be configured to pass the atoms
		that it calculates so that they don't have to be
		recalculated later if they're also needed by whatever
		needs the center of mass.
		"""
		
		atoms = self.atoms()
		com = Vector.zero(3)

		for atom in atoms:
			com += atom.location * atom.mass

		com /= sum([atom.mass for atom in atoms])

		if giveAtoms:
			return com, atoms
		return com
	
	def rotationalInertia(self, giveAtoms: bool=False, giveCoM: bool=False) -> Vec3:
		"""
		Rotational inertia: L = m_i * r_i^2
		"""
		
		com, atoms = self.centerOfMass(giveAtoms=True)

		I = 0
		for atom in atoms:
			m, r = atom.mass, abs(atom.location - com)
			I += m * (r ** 2)

		if giveCoM and giveAtoms:
			return I, atoms, com
		if giveCoM:
			return I, com
		if giveAtoms:
			return I, atoms
		return I
	
	def gamma(self) -> Scalar:
		return Decimal(1 / sqrt(1 - ((abs(self.velocity) ** 2) / c2)))
	
	@property
	def mass(self) -> Scalar:
		"""
		Mass property, automatically accounting for
		special relativity.
		"""
		
		return self.restMass
	
	@mass.getter
	def mass(self) -> Scalar:
		return self.restMass * self.gamma()
	
	@mass.setter
	def mass(self, value: Scalar) -> None:
		self.restMass = value
	
	# Momenta & Kinematics

	def linearMomentum(self) -> Vec3:
		"""
		Linear momentum: p = mv
		"""

		return self.velocity * self.mass
	
	def angularMomentum(self) -> Vec3:
		"""
		Angular momentum: L = I * omega
		"""

		return self.spin * self.rotationalInertia()
	
	def calculateEffects(self, force: Vec3, offset: Vec3) -> tuple[Vec3, Vec3]:
		"""
		Takes a force and the offset at which the force is applied
		(relative to the CoM) and returns the linear and angular
		accelerations on the entity.
		"""
		a = force / self.mass

		if self.POINT:
			return (a, Vector.zero(3))

		I, com = self.rotationalInertia(giveCoM=True)

		r = (offset - com)
		tau = r.cross(force)
		omega = tau / I

		return a, omega
	
# ===== Implementations ===== #

@Entity.register("Particle")
class Particle(Entity):
	
	POINT = True

	def atoms(self) -> None:
		return [Atom(self, self.name, self.location, self.mass, self.charges)]