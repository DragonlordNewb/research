from kolibri.metric import Metric
from kolibri.body import Body
from kolibri.body import Atom
from kolibri.field import Field
from kolibri.utils import *

import gc

class Spacetime:

	NOT_ENABLED = "not enabled"
	RESOLVE_BODIES = "resolve bodies"
	RESOLVE_ATOMS = "resolve atoms"

	BAD_METRIC_TYPE = SystemFailure(SystemFailure.FATAL, "Bad metric type.", "The metric type provided is not of type kolibri.metric.Metric or NoneType.\nOnly Metric objects or None can be provided.")
	FIELDS_NOT_ENABLED = SystemFailure(SystemFailure.NONFATAL, "Fields not enabled.", "May cause anomalous behavior in spacetime simulation to tick this way.")

	class ComponentManager:
		TYPE: type
		DUPLICATES_ALLOWED: bool

		BAD_TYPE = SystemFailure(SystemFailure.NONFATAL, "Bad type.", "Can\'t use such a type with this ComponentManager.\nOperation cancelled.")

		def __init__(self, spacetime: "Spacetime") -> None:
			self.items = []
			self.spacetime = spacetime

		def __len__(self) -> int:
			return len(self.items)

		def __contains__(self, item: object) -> bool:
			itemHash = hash(item)
			for otherItem in self:
				if hash(otherItem) == itemHash:
					return True
			return False

		def __iter__(self) -> Iterable[Any]:
			return iter(self.items)

		# Insert an object into the manager

		def __lshift__(self, item: object) -> None:
			if not issubclass(type(item), self.TYPE):
				self.BAD_TYPE.panic()
				return

			if item not in self or self.DUPLICATES_ALLOWED:
				item.spacetime = self.spacetime
				self.items.append(item)

		def __rrshift__(self, item: object) -> None:
			return self << item

		# Remove an object from the manager, directly or by hash

		def __rshift__(self, item: Union[object, int]) -> None:
			if type(item) == int:
				targetHash = item
			elif type(item) == self.TYPE:
				targetHash = hash(item)
			else:
				self.BAD_TYPE.panic()

			index: int = None
			for i, otherItem in enumerate(self):
				if hash(otherItem) == targetHash:
					index = i
					break

			if index != None:
				item = self.pop(index)
				item.spacetime = None

		def __rlshift__(self, item: Union[object, int]) -> None:
			self >> item

	class BodyManager(ComponentManager):
		TYPE = Body
		DUPLICATES_ALLOWED = True

	class FieldManager(ComponentManager):
		TYPE = Field
		DUPLICATES_ALLOWED = False

	def __init__(self, resolution: Scalar=Decimal(0.000001), memoryAllowance: int=1000 * 1024 * 1024) -> None:
		self._metric: Metric = None
		self.bodies = self.BodyManager(self)
		self.fields = self.FieldManager(self)
		self.resolution = Decimal(resolution)
		self.calculus = Calculus(self.resolution)
		self.memoryAllowance = memoryAllowance

	def __repr__(self) -> str:
		if self.metric == None:
			m = "Metricless"
		else:
			mc = self.metric
			m = type(mc).__name__
		return "<" + m + " Spacetime with " + repr(len(self.bodies)) + " bodies>"

	@property
	def metric(self) -> None:
		return

	@metric.setter
	def metric(self, m: Metric) -> None:
		if not issubclass(type(m), Metric):
			self.BAD_METRIC_TYPE.panic()

		if self._metric != None:
			self._metric.spacetime = None
			self._metric = None

		self._metric = m
		self._metric.spacetime = self

	@metric.getter
	def metric(self) -> Union[Metric, None]:
		return self._metric
	
	@property
	def atoms(self) -> None:
		return
	
	@atoms.setter
	def atoms(self, value: Any) -> Exception:
		raise SyntaxError("Can\'t directly set atoms property of Spacetime.")
	
	@atoms.getter
	def atoms(self) -> Iterable[tuple[Body, Atom]]:
		for body in self.bodies:
			for atom in body.atoms():
				yield (body, atom)

	# Functionality methods

	def tick(self, iterations: int=1, fieldMode: bool=True, _fieldNotEnabledWarned: bool=False, pbar: bool=False) -> None:
		# bread recursion
		if iterations > 1:
			if pbar:
				iterator = ProgressBar(range(iterations))
			else:
				iterator = range(iterations)

			for iteration in iterator:

				self.tick(iterations=1, _fieldNotEnabledWarned=_fieldNotEnabledWarned)
				if _fieldNotEnabledWarned == False:
					_fieldNotEnabledWarned = True

			return

		if not fieldMode:
			if not _fieldNotEnabledWarned:
				self.FIELDS_NOT_ENABLED.panic()
		else:
			for body, atom in self.atoms:
				for field in self.fields:
					if field.signature.issubset(atom.signature):
						force = self.calculus.gradient(lambda v: field.potential(self, v), atom.location) * -1 * self.resolution
						acceleration = field.coupling(atom) * force / atom.mass
						body.accelerate(acceleration * self.resolution)

		for body in self.bodies:
			body.tick(self.resolution)

		del iterations
		del fieldMode
