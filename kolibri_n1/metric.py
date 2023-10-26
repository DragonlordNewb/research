from kolibri.utils import *

class Metric:

	"""
	The Metric class represents a spacetime metric.
	A list-of-lists represents the metric tensor, which in
	turn is used to generate uniaxial, biaxial, and uniform
	warp factors at given points.

	The Metric.tensor variable is used also. Each callable in
	the list of lists must accept the a Kolibri spacetime object,
	a location 3-vector, and a displacement 4-vector, and return
	a scalar value.
	"""

	tensor: list[list[Callable[["Spacetime", Vec3, Vec4], Scalar]]] = None

	def __init__(self) -> None:
		self._spacetime: "Spacetime" = None
		if self.tensor == None:
			raise SyntaxError("Can\'t use the base Metric class.")

	def __getitem__(self, index: tuple[int, int]) -> Callable[["Spacetime", Vec3, Vec4], Scalar]:
		if type(index) == int:
			return self[index, index] # allows getting diags
		mu, nu = index
		return self.tensor[nu][mu] # column-major

	@property
	def spacetime(self) -> None:

		"""
		Metric.spacetime property. Allows the metric to
		automatically install itself when the metric is
		set with "metric.spacetime = <your spacetime>".
		"""

		return self._spacetime

	@spacetime.getter
	def spacetime(self) -> None:
		return self._spacetime

	@spacetime.setter
	def spacetime(self, value: Union["Spacetime", None]) -> None:
		self._spacetime = value
		if value is not None:
			self._spacetime._metric = self

	def warp(self, location: Vec3, displacement: Vec4) -> None:

		"""
		Using all components of the metric tensor (including
		off-diagonal components), calculate the warp at the given point.
		"""

		w = Vector.zero(4)

		# i think this is how it works?

		for mu in range(4):
			for nu in range(4):
				if mu == nu:

					# On-diagonal components: the square root of the
					# factor is applied to the axis to produce a 
					# uniaxial warp of that magnitude

					f = sqrt(self[mu, nu](self.spacetime, location, displacement))
					displacement[]