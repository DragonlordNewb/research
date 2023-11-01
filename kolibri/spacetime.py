"""
Core of the package.
"""

from kolibri.utils import *
from kolibri.entity import *
from kolibri.force import *
from kolibri.metric import *

import decimal
decimal.getcontext().prec = 12

class Spacetime:

	"""
 	As close to a god class as it gets.
	"""
	
	def __init__(self, resolution: Scalar=0.000001) -> None:
		self.resolution = Decimal(resolution)
		self.calculus = Calculus(resolution)
		self.entities: list[Entity] = []
		self.forces: list[Force] = []
		self._metric: Metric = None
		
	@property
	def metric(self) -> Metric:
		"""
		Metric property.
		"""
		
		return self._metric
		
	@metric.getter
	def metric(self) -> Metric:
		return self._metric
		
	@metric.setter
	def metric(self, value: Metric) -> None:
		self._metric = value
		if value is not None:
			self._metric._spacetime = self # shouldn't cause issues

	# Ease-of-access

	def atoms(self) -> Iterable[Atom]:
		for entity in self.entities:
			for atom in entity.atoms():
				yield atom

	def otherAtoms(self, atom: Atom) -> Iterable[Atom]:
		for otherAtom in self.atoms():
			if otherAtom == atom:
				continue
			yield otherAtom

	def __lshift__(self, item) -> None:
		t = type(item)
		if issubclass(t, Metric):
			self.metric = item
			return
		if issubclass(t, Entity):
			self.entities.append(item)
			return
		if issubclass(t, Force):
			self.forces.append(item)
			item.spacetime = self
			return
		raise TypeError("Can\'t add whatever that is.")
		
	def __rrshift__(self, item) -> None:
		return self << item
		
	def tick(self, iterations: int=1) -> None:
		if iterations > 1:
			for _ in ProgressBar(range(iterations)):
				self.tick(1)
			return

		for entity in self.entities:

			ws = []
			for atom in entity.atoms():
				x, y, z = atom.location
				ws.append(self.metric.warp(atom, Vec4(self.resolution, x, y, z)))
			w = Vector.zero(4)
			for _w in ws:
				w += _w / len(ws)
				
			for force in self.forces:
				f, o = force.entityForce(entity)
				a, omega = entity.calculateEffects(f, o)

				for mu in range(3):
					entity.velocity[mu] += a[mu] * w[0] * w[mu + 1] * self.resolution
					entity.spin[mu] += omega[mu] * w[0] * w[mu + 1] * self.resolution

			for mu in range(3):

				entity.location[mu] += entity.velocity[mu] * w[0] * w[mu + 1] * self.resolution
				entity.angle[mu] += entity.spin[mu] * w[0] * w[mu + 1] * self.resolution

	def trace(self, eid: str, ticks: int) -> None:
		ent: Entity = None
		for possibleEntity in self.entities:
			if possibleEntity.name == eid:
				ent = possibleEntity
				break
		if ent is None:
			print("Error: no such entity.")
			return 1
		for i in range(ticks):
			print(
				"\r" + eid, "- at", repr(ent.location), "with velocity", repr(ent.velocity), 
				end=f" ({(i / ticks) * 100:.1f}%)" + (" " * 10)
			)
			self.tick(1)
		print("")