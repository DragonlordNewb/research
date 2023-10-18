from kolibri.metric.engine import Metric

from kolibri.utils import *

@Metric.register("minkowski")
class Minkowski(Metric):
	def timewarp(self, location: Vector) -> int:
		return 1
	
	def spacewarp(self, location: Vector) -> int:
		return 1