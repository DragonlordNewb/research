from kolibri.utils import *
from kolibri.general.field import Field

class QuantumWave:
	def __init__(self, minimum: Vec3, maximum: Vec3, resolution: Scalar=Decimal("1e-12")):
		self.positionAmplitude = Field(minimum, maximum, resolution)
		self.velocityAmplitude = Field(minimum, maximum, resolution)