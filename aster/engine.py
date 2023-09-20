from abc import ABC
from abc import abstractmethod

class Spacetime:
	"""
 	A Python representation of spacetime.

 	Requires a single parameter, "metric", which
	must be an aster.engine.Metric object. This metric
 	will govern the behavior of the spacetime's geometry.
	"""

