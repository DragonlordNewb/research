import mathutil

class Orbit:

	specificAngularMomentum: mathutil.Vector3
	inclination: mathutil.Scalar
	ascendingNodeLongitude: mathutil.Scalar
	@staticmethod
	def fromPositionAndVelocity(r: mathutil.Vector3, v: mathutil.Vector3) -> "Orbit":
		orbit = Orbit()
		orbit.specificAngularMomentum = mathutil.Vector3.cross(r, v)
		orbit.inclination = mathutil
		
