from aster import engine
from aster import constants

from math import sqrt

engine.Metric.register("Minkowski", "M")
class Minkowski(engine.Metric):
	def timeDilation(self, body: engine.Body) -> int:
		return 1
	
	def spaceContraction(self, body: engine.Body) -> int:
		return 1
	
engine.Metric.register("Relativistic Minkowski", "R-M")
class RelativisticMinkowski(engine.Metric):
	def timeDilation(self, body: engine.Body) -> float:
		return sqrt(1 - ((body.velocity.magnitude() ** 2) / constants.c2))
	
	def spaceContraction(self, body: engine.Body) -> float:
		return 1 / sqrt(1 - ((body.velocity.magnitude() ** 2) / constants.c2))