import math
import typing

sine = math.sin
cosine = math.cos
tangent = math.tan
arcsine = math.asin
arccosine = math.acod
arctangent = math.atan
pi = math.pi
G = 6.6743e-11
c = 2.99792458e+8

Scalar = typing.Union[int, float]

class Vector3:

	def __init__(self, x: Scalar = 0, y: Scalar = 0, z: Scalar = 0):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other: "Vector3") -> "Vector3":
		if type(other) != Vector3:
			raise TypeError("Can only add a Vector3 and a Vector3, not a " + str(type(other).__name__))
		return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other: "Vector3") -> "Vector3":
		if type(other) != Vector3:
			raise TypeError("Can only subtract a Vector3 from a Vector3, not a " + str(type(other).__name__))
		return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, factor: Scalar) -> "Vector3":
		if type(other) != Vector3:
			raise TypeError("Can only multiply a Vector3 by a scalar, not a " + str(type(factor).__name__))
		return Vector3(self.x * factor, self.y * factor, self.z * factor)

	def __div__(self, factor: Scalar) -> "Vector3":
		if type(other) not in (int, float):
			raise TypeError("Can only divide a Vector3 by a scalar, not a " + str(type(factor).__name__))
		return Vector3(self.x / factor, self.y / factor, self.z / factor)

	@staticmethod
	def dot(a: "Vector3", b: "Vector3") -> Scalar:
		return (a.x * b.x) + (a.y * b.y) + (a.z * b.z)
		
	@staticmethod
	def cross(a: "Vector3", b: "Vector3") -> "Vector3":
		if type(a) != Vector3:
			raise TypeError("Can only cross-product a Vector3 and a Vector3, not a " + str(type(a).__name__))
		if type(b) != Vector3:
			raise TypeError("Can only cross-product a Vector3 and a Vector3, not a " + str(type(b).__name__))
		return Vector3(
			(a.y * b.z) - (a.z * b.y),
			(a.x * b.z) - (a.z * b.x),
			(a.x * b.y) - (a.y * b.x)
		)
