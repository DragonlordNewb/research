from kolibri.metric import Metric
from kolibri.body import Body
from kolibri.field import Field
from kolibri.utils import *

class Spacetime:

	BAD_METRIC_TYPE = SystemFailure(SystemFailure.FATAL, "Bad metric type.", "The metric type provided is not of type kolibri.metric.Metric or NoneType.\nOnly Metric objects or None can be provided.")

	class ComponentManager:
		TYPE: type
		DUPLICATES_ALLOWED: bool

		BAD_TYPE = SystemFailure(SystemFailure.NONFATAL, "Bad type.", "Can\'t use such a type with this ComponentManager.\nOperation cancelled.")

		def __init__(self, spacetime: "Spacetime") -> None:
			self.items = []
			self.spacetime = spacetime

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
	
	def __init__(self, resolution: Scalar=0.000001) -> None:
		self._metric: Metric = None
		self.bodies = self.BodyManager(self)
		self.fields = self.FieldManager(self)
		self.resolution = resolution

	@property
	def metric(self) -> None:
		return
	
	@metric.setter
	def metric(self, m: Metric) -> None:
		if not issubclass(type(m), Metric):
			self.BAD_METRIC_TYPE.panic()
		if self._metric != None:
			self._metric._spacetime = None
			self._metric = None

		self.metric = m

	@metric.getter
	def metric(self) -> Union[Metric, None]:
		return self._metric
	
	# Functionality methods
	
	def tick(self, fieldsEnabled: bool=True) -> None:
		if fieldsEnabled:
			pass
		
		for body in self.bodies:
			body.tick(self.resolution)