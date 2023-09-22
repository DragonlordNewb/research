from typing import Iterable

from math import sqrt

class Vector:
	def __init__(self, x: float, y: float, z: float) -> None:
		self.x, self.y, self.z = x, y, z

	def __repr__(self) -> str:
		return "<" + ", ".join(map(repr, self)) + ">"
	
	def __iter__(self) -> Iterable[float]:
		return iter((self.x, self.y, self.z))

	def __add__(self, other: "Vector") -> "Vector":
		return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
	
	def __iadd__(self, other: "Vector") -> "Vector":
		return self + other

	def __sub__(self, other: "Vector") -> "Vector":
		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
	
	def __isub__(self, other: "Vector") -> "Vector":
		return self - other
	
	def __mul__(self, factor: float) -> "Vector":
		return Vector(self.x * factor, self.y * factor, self.z * factor)
	
	def __imul__(self, factor: float) -> "Vector":
		return self * factor
	
	def __truediv__(self, factor: float) -> "Vector":
		return Vector(self.x / factor, self.y / factor, self.z / factor)
	
	def __itruediv__(self, factor: float) -> "Vector":
		return self / factor
	
	def __abs__(self) -> float:
		return sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))