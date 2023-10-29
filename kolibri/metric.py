from kolibri.utils import *

from functools import lru_cache

def const(value: Scalar) -> Callable[[Vec3, Vec4, "Spacetime"], Scalar]:
	def _const(*args, **kwargs):
		return value
	return _const

ZERO = const(0)
ONE = const(1)

class Metric:

	tensor: list[list[Callable[[Vec3, Vec4, "Spacetime"], Scalar]]]

	def __init__(self) -> None:
		self._spacetime = None

	@property
	def spacetime(self) -> "Spacetime":
		return self._spacetime
	
	@spacetime.getter
	def spacetime(self) -> "Spacetime":
		return self._spacetime
	
	@spacetime.setter
	def spacetime(self, value: Union["Spacetime", None]) -> None:
		self._spacetime == value
		if value is not None:
			self._spacetime._metric = self

	def __getitem__(self, index: tuple[int, int]) -> Callable:
		mu, nu = index
		return self.tensor[nu][mu]
	
	def warp(self, l: Vec3, dX: Vec4) -> Vec4:
		W = Vector.zero(4)

		for nu, column in enumerate(self.tensor):
			for mu, component in enumerate(column):
				f = component(l, dX, self.spacetime)
				g = sqrt(f)

				if mu == nu:
					W[mu] += g
				else:
					W[mu] += g
					W[nu] += g

		return Vec4(*[w * dx for w, dx in zip(W, dX)])
	
# ===== Implementations ===== #

class Minkowski(Metric):
	
	tensor = [
		[const(-c2), ZERO, ZERO, ZERO],
		[ZERO,       ONE,  ZERO, ZERO],
		[ZERO,       ZERO, ONE,  ZERO],
		[ZERO,       ZERO, ZERO, ONE ]
	]

class Schwarzschild(Metric):

	@lru_cache(maxsize=5)
	@staticmethod
	def factor(l: Vec3, dX: Vec4, spacetime: "Spacetime") -> Scalar:
		f = 1
		for atom in spacetime.atoms():
			if atom.location == l:
				continue
			r = abs(l - atom.location)
			f *= 1 - ((2 * G * atom.mass) / (r * c2))
		return Decimal(f)
	
	@lru_cache(maxsize=5)
	@staticmethod
	def invfactor(l, dX, spacetime):
		return 1 / Schwarzschild.factor(l, dX, spacetime)
	
	tensor = [
		[factor, ZERO,      ZERO,      ZERO     ],
		[ZERO,   invfactor, ZERO,      ZERO     ],
		[ZERO,   ZERO,      invfactor, ZERO     ],
		[ZERO,   ZERO,      ZERO,      invfactor]
	]

class ReissnerNordstrom(Metric):
	# Apologize for misspelling Nordstrom's name.
	# The Python interpreter doesn't like Unicode.

	@lru_cache(maxsize=5)
	@staticmethod
	def factor(l: Vec3, dX: Vec4, spacetime: "Spacetime") -> Scalar:
		f = 1
		for atom in spacetime.atoms():
			if atom.location == l:
				continue
			r = abs(l - atom.location)
			f *= (1 - ((2 * G * atom.mass) / (r * c2))) + (((atom.charge ** 2) * G) / (4 * pi * epsilon0 * c4 * (r ** 2)))
		return Decimal(f)
	
	@lru_cache(maxsize=5)
	@staticmethod
	def invfactor(l, dX, spacetime):
		return 1 / ReissnerNordstrom.factor(l, dX, spacetime)
	
	tensor = [
		[factor, ZERO,      ZERO,      ZERO     ],
		[ZERO,   invfactor, ZERO,      ZERO     ],
		[ZERO,   ZERO,      invfactor, ZERO     ],
		[ZERO,   ZERO,      ZERO,      invfactor]
	]
