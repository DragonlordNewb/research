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
