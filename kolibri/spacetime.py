from kolibri.metric import *
from kolibri.entity import *
from kolibri.constants import *
from kolibri.utils import *

class Spacetime:
	
	"""
	More or less Kolibri's god class, allows for the addition
	of entities to a simulation of a particular spacetime metric
	in addition to different fields that act between objects.
	"""

	def __init__(self) -> None:
		self._metric = None
		self.forces = []
		self.entities = []

	def addEntity(self, entity: Entity) -> None:
		self.entities.append(entity)