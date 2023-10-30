from kolibri.metric import *
from kolibri.entity import *
from kolibri.forces import *
from kolibri.constants import *
from kolibri.utils import *

class Spacetime:
	
	"""
	More or less Kolibri's god class, allows for the addition
	of entities to a simulation of a particular spacetime metric
	in addition to different fields that act between objects.
	"""

	def __init__(self, h: Scalar=Decimal(0.000001)) -> None:
		self._metric = None
		self.forces = []
		self.entities = []

		self.h = h
		self.calculus = Calculus(h)

	@property
	def metric(self) -> None:
		""" 
		Spacetime.metric property.
		"""

	@metric.getter
	def metric(self) -> Metric:
		return self._metric
	
	@metric.setter
	def metric(self, value: Metric) -> None:
		self._metric = value 
		if value != None:
			self._metric._spacetime = self # shouldn't casue problems

	def addEntity(self, entity: Entity) -> None:
		self.entities.append(entity)

	def addForce(self, force: Force) -> None:
		self.forces.append(force)

	def atoms(self) -> Iterable[Entity.Atom]:
		for entity in self.entities:
			for atom in entity.atoms():
				yield atom

	def otherAtoms(self, atom: Atom) -> Iterable[Entity.Atom]:
		for entity in self.entities:
			if entity == atom.parent:
				continue
			for atom in self.entity.atoms():
				yield atom

	def tick(self, iterations: int=1) -> None:
		"""
		Tick the simulation forward a given number of times.
		"""

		if iterations > 1:
			for _ in range(iterations - 1):
				self.tick(1)

		for entity in self:

			deltaV, deltaOmega = Decimal(0)
			forces: list[tuple[Vector, Vector]] = []

			for atom in entity.atoms():
				for force in self.forces:
					forces.append(force.apply(atom))

			appliedForce = Vector(0, 0, 0)
			forceLocation = Vector(0, 0, 0)
			for f, o in forces:
				appliedForce += f
				forceLocation += o
			appliedForce /= len(forces)
			forceLocation /= len(forces)

			entity.applyForce(appliedForce, forceLocation, self.h)

		for entity in self:
			warp = self.metric.warp(entity.location)

			entity.location += warp * entity.velocity * self.h
			entity.angle += warp * entity.rotation * self.h