from kolibri.constants import *
from kolibri.utils import *

# There are two types of forces: the Interaction
# and the Field.
#
# Interactions exert forces between only interacting
# particles by calculating the exerted force between
# all n^2 - n pairs of interacting particles.
#
# Fields exert forces between only coupled particles
# by calculating the field potential at the location
# of each of the n particles and using a gradient to
# determine the direction and magnitude of the force.

class Force(ABC):

	"""
	The Force is an abstract base class for the
	Interaction and the Field classes exclusively.
	Do not use.
	"""

	def __init__(self, **parameters):
		self.parameters = parameters

	
