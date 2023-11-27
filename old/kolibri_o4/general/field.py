from kolibri.utils import *

class Field:

	def __init__(self, minimum: Vec3, maximum: Vec3, resolution: Scalar=Decimal("1e-12"), generator: Callable[[Vec3], Any]=None):
		if generator is None:
			generator = self._zeros
		self.locations = {
			x: {
				y: {
					z: generator(Vec3(x, y, z)) for z in range(minimum.z, maximum.z, float(resolution))
				} for y in range(minimum.y, maximum.y, float(resolution))
			} for x in range(minimum.x, maximum.x, float(resolution))
		}
		self.ix = self.iy = self.iz = 0
		self.minimum = minimum
		self.maximum = maximum
		self.resolution = resolution
		self.generator = generator

	@staticmethod
	def _zeros(location: Vec3) -> Scalar:
		return Decimal(0)
	
	def __getitem__(self, indices: tuple[Scalar, Scalar, Scalar]) -> Scalar:
		x, y, z = indices
		return self.locations[x][y][z]
	
	def __iter__(self) -> Iterable[tuple[Vec3, Scalar]]:
		return self
	
	def __next__(self) -> tuple[Vec3, Scalar]:
		for x in self.locations.keys():
			for y in self.locations[x].keys():
				for z in self.locations[x][y].keys():
					yield (Vec3(x, y, z), self[x, y, z])
		raise StopIteration