"""
Metric classes and implementations.

Note that -+++ signature is used.
"""

from kolibri.utils import *
from kolibri.constants import *
from kolibri.entity import *

class Component(ABC):

	"""
	Simple class representative of metric tensor 
	components.
	"""

	CONSTANT: Scalar = None

	def __call__(self, atom: Atom, displacement: Vec4, spacetime: "Spacetime") -> Scalar:
		if hasattr(self, "axial"):
			return self.axial(atom, displacement, spacetime)
		return self.CONSTANT
	
	@classmethod
	def constant(cls, value: Scalar) -> "Component":
		"""
		Generate a constant Component.
		"""

		class ConstantComponent(cls):

			CONSTANT = Decimal(value)

		return ConstantComponent()
	
ZERO = Component.constant(0)
ONE = Component.constant(1)

class Metric:

	"""
	Singlehandedly represents a spacetime metric!
	Subclasses need only provide the Metric.tensor
	list of lists of callables, and the Metric will 
	do the rest.

	Each Callable must accept three arguments: a
	Vec3, a Vec4, and a Spacetime in that order,
	and should return a scalar. The arguments
	respectively represent the object in question,
	the particular displacement of the object 
	in question, and lastly the spacetime in which 
	the object is embedded. The return value is 
	the given component of the metric tensor.
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

	tensor: list[list[Component]] = None
	
	def __init__(self, h: Scalar=0.001) -> None:
		if self.tensor is None:
			raise NotImplementedError("Can\'t use the Metric base class.")
		
		self._spacetime: "Spacetime" = None

		self.OFF_DIAGONALS = False

		for mu in range(4):
			for nu in range(4):
				if mu == nu:
					continue
				
				if self[mu, nu].CONSTANT not in [0, None]:
					self.OFF_DIAGONALS = True
					return
				
		self.calculus = Calculus(h)

	def __getitem__(self, index: tuple[int, int]) -> Component:
		"""
		Get components.

		Row-major, by the way.
		"""

		mu, nu = index
		return self.tensor[nu][mu]

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
		Set the spacetime of the metric.
		Equivalent to setting the metric of the spacetime.
		"""

		self._spacetime = spacetime
		if spacetime is not None:
			self._spacetime._metric = self # probably won't cause issues

	def warp(self, atom: Atom, displacement: Vec4) -> Scalar:
		"""
		Calculate the four-warp vector for a given particle
		with its displacement.
		"""

		w: Vec4 = Vector.zero(4)

		if self.spacetime is None:
			raise RuntimeError("Missing a Spacetime.")
		
		# Calculate and add uniaxial warps
		for mu in range(4):
			gmm = self[mu, mu](atom, displacement, self.spacetime)
			if mu == 0:
				w[mu] += Decimal(sqrt(-gmm))
				continue
			w[mu] += Decimal(sqrt(gmm))

		if not self.OFF_DIAGONALS:
			return w

		# Calculate and add biaxial warps
		for mu in range(4):
			for nu in range(4):
				if mu == nu:
					continue
				
				gmn = self[mu, nu](atom, displacement, self.spacetime)
				gnm = self[nu, mu](atom, displacement, self.spacetime)
				s = gmn + gnm
				w[mu] += s / displacement[nu]
				w[nu] += s / displacement[mu]

		return w
	
	def distance(self, atom: Atom, a: Vec3, b: Vec3) -> Scalar:
		d = b - a
		dx = d.x
		dy = d.y
		dz = d.z
		w = self.warp(atom, d)
		return abs(Vec3(dx * w.x, dy * w.y, dz * w.z))
	
# ===== Implementations ===== #

@Metric.register("Minkowski")
class Minkowski(Metric):

	"""
	Minkowski space: flat spacetime.
	"""

	g00 = Component.constant(-(c ** 2))
	gii = Component.constant(1)

	tensor = [
		[g00,  ZERO, ZERO, ZERO],
		[ZERO, gii,  ZERO, ZERO],
		[ZERO, ZERO, gii,  ZERO],
		[ZERO, ZERO, ZERO, gii ]
	]

@Metric.register("Schwarzschild")
class Schwarzschild(Metric):

	"""
	Schwarzschild metric: accounts for mass.
	"""

	class Schwarzschild00(Component):
		def axial(self, atom, displacement, spacetime):
			w = 1
			for otherAtom in spacetime.otherAtoms(atom):
				w *= -1 * (1 - ((2 * G * otherAtom.mass) / (abs(otherAtom.location - atom.location) * c2)))
			return w
		
	class SchwarzschildSS(Component):
		def axial(self, atom, displacement, spacetime):
			w = 1
			for otherAtom in spacetime.otherAtoms(atom):
				w *= 1 / (1 - ((2 * G * otherAtom.mass) / (abs(otherAtom.location - atom.location) * c2)))
			return w
		
	tensor = [
		[Schwarzschild00(), ZERO,              ZERO,              ZERO             ],
		[ZERO,              SchwarzschildSS(), ZERO,              ZERO             ],
		[ZERO,              ZERO,              SchwarzschildSS(), ZERO             ],
		[ZERO,              ZERO,              ZERO,              SchwarzschildSS()]
	]