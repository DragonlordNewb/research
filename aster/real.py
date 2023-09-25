# Advanced SpaceTime Engineering Research software realism component.
# Adds various real metrics and constants to the Universe.

from aster.engine import Metric

class Minkowski(Metric):
	def spaceContraction(self, location):
		return 1

	def timeDilation(self, location):
		return 1

