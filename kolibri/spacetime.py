from kolibri.metric import Metric
from kolibri.utils import *

class Spacetime:

	BAD_METRIC_TYPE = SystemFailure(SystemFailure.FATAL, "Bad metric type.", "The metric type provided is not of type kolibri.metric.Metric or NoneType.\nOnly Metric objects or None can be provided.")

	def __init__(self) -> None:
		self._metric: Metric = None
		self.bodies = []
		self.fields = []

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