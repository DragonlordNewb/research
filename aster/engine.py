from abc import ABC
from abc import abstractmethod

class Body(ABC):
	"""
 	A Python representation of a physical object.
	"""

	@abstractmethod
	def points(self) -> None:
		pass

class Metric(ABC):
	"""
 	A Python representation of a spacetime metric.
  	Must adequately be subclassed to describe how an
   	object experiences time dilation, space contraction,
    	etc.
     	"""

	@abstractmethod
	def timeDilation(self, object: 

class Spacetime:
	"""
 	A Python representation of spacetime.

 	Requires a single parameter, "metric", which
	must be an aster.engine.Metric object. This metric
 	will govern the behavior of the spacetime's geometry.
	"""

	def __init__(self, metric: Metric) -> None:
		
