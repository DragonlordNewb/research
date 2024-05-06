import mathutil
import orbit

DEFAULT_NEW_NAME = "New Celestial Body"

class CelestialBody:

	name: str
	mass: mathutil.Scalar
	radius: mathutil.Scalar
	sgp: mathutil.Scalar
	
	@staticmethod
	def fromMassAndRadius(mass: mathutil.Scalar, radius: mathutil.Scalar, name: str = DEFAULT_NEW_NAME) -> "CelestialBody":
		cb = CelestialBody()
		cb.name = name
		cb.mass = mass
		cb.radius = radius
		cb.sgp = mass * mathutil.G
		
	@staticmethod 
	def fromSGPAndRadius(sgp: mathutil.Scalar, radius: mathutil.Scalar, name: str = DEFAULT_NEW_NAME) -> "CelestialBody":
		cb = CelestialBody()
		cb.name = name
		cb.mass = sgp / mathutil.G
		cb.radius = radius
		cb.sgp = sgp
