import mathutil
import orbit

DEFAULT_NEW_NAME = "New Celestial Body"

ESCAPE = "ESCAPE"
REENTRY = "REENTRY"
PARKING = "PARKING"
COLLISION = "COLLISION"
AEROBRAKE = "AEROBRAKE"
STABLE = "STABLE"
UNSTABLE = "UNSTABLE"

class CelestialBody:

	name: str
	mass: mathutil.Scalar
	radius: mathutil.Scalar
	sgp: mathutil.Scalar
	hasAtmosphere: bool = False
	atmosphericHeight: mathutil.Scalar = None
	lowestOrbit: mathutil.Scalar = None
	
	@staticmethod
	def fromMass(
		mass: mathutil.Scalar, 
		radius: mathutil.Scalar, 
		name: str = DEFAULT_NEW_NAME,
		atmosphericHeight: mathutil.Scalar = None
	) -> "CelestialBody":
		cb = CelestialBody()
		cb.name = name
		cb.mass = mass
		cb.radius = radius
		cb.sgp = mass * mathutil.G
		if atmosphericHeight is not None:
			hasAtmosphere = True
			self.atmosphericHeight = atmosphericHeight
			self.lowestOrbit = self.atmosphericHeight + self.radius
		
	@staticmethod 
	def fromSGP(
		sgp: mathutil.Scalar, 
		radius: mathutil.Scalar, 
		name: str = DEFAULT_NEW_NAME,
		atmosphericHeight: mathutil.Scalar = None
	) -> "CelestialBody":
		cb = CelestialBody()
		cb.name = name
		cb.mass = sgp / mathutil.G
		cb.radius = radius
		cb.sgp = sgp
		if atmosphericHeight is not None:
			hasAtmosphere = True
			self.atmosphericHeight = atmosphericHeight
			self.lowestOrbit = self.atmosphericHeight + self.radius
			
	def orbitType(self, o: orbit.Orbit) -> tuple[str, str]:
		pe = o.periapsis
		e = o.eccentricity
		if not self.hasAtmosphere:
			if pe <= self.radius:
				return (STABLE, COLLISION)
			if e >= 1:
				return (STABLE, ESCAPE)
			if e < 1:
				return (STABLE, PARKING)
		else:
			if e >= 1:
				if pe <= self.radius:
					return (UNSTABLE, COLLISION)
				if pe <= self.lowestOrbit:
					return (UNSTABLE, AEROBRAKE)
				return (STABLE, ESCAPE)
			else:
				if pe <= self.radius:
					return (UNSTABLE, COLLISION)
				if pe <= self.lowestOrbit:
					return (UNSTABLE, REENTRY)
				return (STABLE, PARKING)
				
	def orbitFromPositionAndVelocity(self, r: mathutil.Vector3, v: mathutil.Vector3) -> orbit.Orbit:
		return orbit.Orbi.fromSGPPositionAndVelocity(self.sgp, r, v)
