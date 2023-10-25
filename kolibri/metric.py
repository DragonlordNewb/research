from kolibri.utils import *
from kolibri.constants import *

# Define this as a sentinel in case something horribly wrong happens
# and an object passes through an event horizon
EVENT_HORIZON_CROSSED = "event horizon crossed"

class Metric(ABC):

	"""
	The Metric abstract base class represents a spacetime metric.
	Two methods need be overridden: the static methods Metric._spacewarp
	and Metric._timewarp. See the abstract methods below for more
	information.

	Once these are overridden, methods like Metric.spacewarp,
	Metric.timewarp, etc. work once the spacetime is set. The 
	Metric has an @property specifically for this purpose.
	"""

	@abstractstaticmethod
	def _spacewarp(spacetime: "Spacetime", location: Vector) -> Scalar:
		"""
		Compute the factor by which space is expanded at a given
		location in a given spacetime.

		W_S > 1 => MORE space is experienced, rulers contract, velocity is lower
		W_S < 1 => LESS space is experienced, rulers expand, velocity is higher
		"""

		pass

	@abstractstaticmethod
	def _timewarp(spacetime: "Spacetime", location: Vector) -> Scalar:
		"""
		Compute the factor by which time is dilated at a given
		location in a given spacetime.

		W_T > 1 => MORE time is experienced, clocks speed up, velocity is higher
		W_T < 1 => LESS time is experienced, clocks slow down, velocity is lower
		"""
		
		pass

	def __init__(self) -> None:
		self._spacetime: "Spacetime" = None

	@property
	def spacetime(self) -> None:
		"""
		Spacetime property.
		"""

		return
	
	@spacetime.getter
	def spacetime(self) -> Union[None, "Spacetime"]:
		"""
		Get the Metric._spacetime attribute.
		"""

		return self._spacetime

	@spacetime.setter
	def spacetime(self, spacetime: "Spacetime") -> None:
		"""
		Set the spacetime of the metric.
		Equivalent to setting the metric of the spacetime.
		"""

		self._spacetime = spacetime
		if spacetime is not None:
			self._spacetime._metric = self # probably won't cause issues

	def spacewarp(self, location: Vector) -> Scalar:
		"""
		Compute the spacewarp factor at a given location.

		Requires that the Spacetime be set.
		"""	
	
		if self.spacetime == None:
			raise RuntimeError("Can\'t compute spacewarp without a Spacetime.")

		return self._spacewarp(self.spacetime, location)

	def timewarp(self, location: Vector) -> Scalar:
		"""
		Compute the timewarp factor at a given location.

		Requires that the Spacetime be set.
		"""

		if self.spacetime == None:
			raise RuntimeError("Can\'t compute timewarp without a Spacetime.")

		return self._timewarp(self.spacetime, location)

# ===== Implementations ===== #

class Minkowski(Metric):

	"""
	Minkowski space: perfectly flat spacetime in which
	no warps take effect.

	ds^2 = -c^2dt^2 + dx^2 + dy^2 + dz^2
	"""

	@staticmethod
	def _spacewarp(spacetime, location):
		return 1

	@staticmethod
	def _timewarp(spacetime, location):
		return 1

class Schwarzschild(Metric):

	"""
	Metric which accounts for mass but not electric charge
	or rotation.

	ds^2 = -(1 - 2Gm/rc^2)c^2dt^2 + (1 - 2Gm/rc^2)^-1 (dx^2 + dy^2 + dz^2)
	"""

	@staticmethod
	def schwarzschildSpaceFactor(m, r):
		return Decimal(1 / schwarzschildTimeFactor(m, r))

	@staticmethod
	def schwarzschildTimeFactor(m, r):
		try:
			return Decimal(1 - (2 * G * m) / (r * c2))
		except:
			return EVENT_HORIZON_CROSSED

	@staticmethod
	def _spacewarp(spacetime, location):
		warp = 1
		for atom in spacetime.atoms():
			warp *= self.schwarzschildSpaceFactor(atom.mass, abs(atom.location - location))
		return warp

	@staticmethod
	def _timewarp(spacetime, location):
		warp = 1
		for atom in spacetime.atoms():
			warp *= self.schwarzschildTimeFactor(atom.mass, abs(atom.location - location))
		return warp