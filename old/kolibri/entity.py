from kolibri.utils import *
from kolibri.constants import *

class Entity(ABC):
	"""
	The Entity class represents the idea of a simple
	object embedded in spacetime: it has axial and angular
	location and velocity, can be accelerated and spun, and
	has arbitrary properties like mass and charge.

	It also has a built-in classifier that allows checking if
	at any given point in spacetime it is "bradyonic", "luxonic",
	or "tachyonic", referring to the whether the ratio of its
	velocity to that of light is less than, equal to, or greater
	than one (respectively). This is useful for analyzing
	potentially-desirable warp!
	"""

	class Atom:
		def __init__(self, parent: "Entity", location: Vector, mass: Scalar, **charges: dict[str, Any]) -> None:
			self.location = location
			self.mass = mass
			self.charges = charges
			self.signature = set(self.charges.keys())

	def __init__(self, id: str, location: Vector, restMass: Scalar=1, **charges: dict[str, Any]) -> None:
		self.id = id

		self.location = location
		self.angle = Vector(0, 0, 0)
		self.velocity = Vector(0, 0, 0)
		self.rotation = Vector(0, 0, 0)

		self.restMass = Decimal(restMass)
		self.charges = charges

		self.signature = set(self.charges.keys())

	def __eq__(self, other: "Entity") -> bool:
		"""
		Check the Entity IDs to see if they're the same.
		"""
		if not issubclass(type(other), type(self)):
			return False
		return self.id == other.id

	def makeAtom(self, *args, **kwargs) -> Atom:
		"""
		Make an Atom, automatically setting the parent to
		this Entity.
		"""

		return self.Atom(self, *args, **kwargs)

	@abstractmethod
	def atoms(self) -> Iterable[Atom]:
		"""
		Produce a set of Atoms which represent this object.
		"""

		pass

	@property
	def gamma(self) -> None:
		"""
		Get the object's relativistic gamma,
		which is the reciprocal of the square root
		of one minus the square of the ratio of the
		object's velocity to that of light. 
		"""

		return

	@gamma.getter
	def gamma(self) -> Scalar:
		beta = abs(self.velocity) / c
		return Decimal(1 / sqrt(1 - (beta ** 2)))

	@gamma.setter
	def gamma(self, value: Any) -> Exception:
		raise SyntaxError("Can\'t set Entity.gamma property.")

	@property
	def mass(self) -> Scalar:
		"""
		Get the mass of the object,
		accounting for relativity.
		"""

		return self.restMass

	@mass.getter
	def mass(self) -> Scalar:
		gamma = self.gamma
		return self.restMass * gamma

	@mass.setter
	def mass(self, value: Any) -> Exception:
		raise SyntaxError("Can\'t set Entity.mass property; try Entity.restMass.")

	@property
	def centerOfMass(self) -> None:
		"""
		Get the center of mass of the object.
		"""

		return

	@centerOfMass.getter
	def centerOfMass(self) -> Vector:
		atoms = self.atoms()
		loc = Vector(0, 0, 0)
		for atom in atoms:
			loc += atom.location
		return loc / len(atoms)

	@centerOfMass.setter
	def centerOfMass(self, value: Any) -> Exception:
		raise SyntaxError("Can\'t set Entity.centerOfMass property.")

	@property
	def rotationalInertia(self) -> None:
		"""
		Get the rotational inertia of the object.
		"""

		return

	@rotationalInertia.getter
	def rotationalInertia(self) -> Scalar:
		com = self.centerOfMass
		I = 0
		for atom in self.atoms():
			r = abs(atom.location - com)
			I += atom.mass * (r ** 2)
		return Decimal(I) if Decimal(I) != 0 else 1

	def applyForce(self, f: Vector, location: Vector, timestep: Scalar, apply: bool=True) -> tuple[Vector, Vector]:
		"""
		Get the angular and linear accelerations given a force
		applied at an offset from the center of mass.
		"""

		offset = location - self.location

		I = self.rotationalInertia
		r = offset - self.location
		tau = r.cross(f)

		deltaOmega = tau * timestep / I
		deltaV = f * timestep / self.mass

		if apply:
			self.velocity += deltaV
			self.rotation += deltaOmega

		return deltaV, deltaOmega
	
# ===== Implementations ===== #

class Particle(Entity):
	def atoms(self) -> list[Entity.Atom]:
		return [self.makeAtom(location=self.location, mass=self.mass, **self.charges)]