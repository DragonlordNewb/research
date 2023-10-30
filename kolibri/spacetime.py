"""
Core of the package.
"""

from kolibri.utils import *
from kolibri.entity import *
from kolibri.force import *
from kolibri.metric import *

class Spacetime:

	"""
 	As close to a god class as it gets.
	"""
	
	def __init__(self, resolution: Scalar=0.000001) -> None:
		self.resolution = resolution
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
	
