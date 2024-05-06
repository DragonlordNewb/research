import mathutil

class Orbit:

	sgp: mathutil.Scalar
	centralBodyMass: mathutil.Scalar
	
	specificAngularMomentum: mathutil.Vector3
	specificOrbitalEnergy: mathutil.Scalar
	
	semiMajorAxis: mathutil.Scalar
	semiMinorAxis: mathutil.Scalar
	semiLatusRectum: mathutil.Scalar
	eccentricity: mathutil.Scalar
	apoapsis: mathutil.Scalar
	periapsis: mathutil.Scalar
	
	inclination: mathutil.Scalar
	ascendingNodeLongitude: mathutil.Scalar
	
	@staticmethod
	def fromSGPPositionAndVelocity(sgp: mathutil.Scalar, r: mathutil.Vector3, v: mathutil.Vector3) -> "Orbit":
		orbit = Orbit()
		orbit.sgp = sgp
		orbit.centralBodyMass = sgp / mathutil.G
		orbit.specificOrbitalEnergy = (abs(v) / 2) - (self.sgp / abs(r))
		orbit.specificAngularMomentum = mathutil.Vector3.cross(r, v)
		orbit.calculateOrbitalParameters()
		return orbit

	@staticmethod
	def fromMassPositionAndVelocity(mass: mathutil.Scalar, r: mathutil.Vector3, v: mathutil.Vector3) -> "Orbit":
		orbit = Orbit()
		orbit.centralBodyMass = sgp
		orbit.sgp = mass * mathutil.G
		orbit.specificOrbitalEnergy = (abs(v) / 2) - (self.sgp / abs(r))
		orbit.specificAngularMomentum = mathutil.Vector3.cross(r, v)
		orbit.calculateOrbitalParameters()
		return orbit

	def calculateOrbitalParameters() -> None:
		self.eccentricity = mathutil.sqrt(
			1 + (
				(2 * specificOrbitalEnergy * (abs(self.specificAngularMomentum) ** 2))
				/ (sgp ** 2)
			)
		)
		self.semiMajorAxis = -1 * (self.sgp / (2 * self.specificOrbitalEnergy))
		self.semiMinorAxis = self.semimajorAxis * mathutil.sqrt(1 - (self.eccentricity ** 2))
		self.semiLatusRectum = self.semiMajorAxis * (1 - (self.eccentricity ** 2))
		
		self.apoapsis = self.semiMajorAxis * (1 + self.eccentricity)
		self.periapsis = self.semiMajorAxis * (1 - self.eccentricity)
		
		self.inclination = mathutil.arccosine(self.specificAngularMomentum.z / abs(self.specificAngularMomentum))
		n = mathutil.Vector3(-1 * self.specificAngularMomentum.y, self.specificAngularMomentum.x, 0)
		if n.y >= 0:
			self.ascendingNodeLongitude = mathutil.arccosine(n.x / abs(n))
		else:
			self.ascendingNodeLongitude = (2 * mathutil.pi) - mathutil.arccosine(n.x / abs(n))
			
