from efesolver import variables

import numpy

class Metric:

	def __init__(self, g0mu, g1mu, g2mu, g3mu):
		self.lower = numpy.array([g0mu, g1mu, g2mu, g3mu])
		self.upper = numpy.linalg.inv(self.lower)

	def sub(self, mu, nu):
		return self.lower[mu][nu]

	def sup(self, alpha, beta):
		return self.upper[alpha, beta]

	def christoffel(self, i, j, k):
		s = 0
		for m in range(4):
			s += 0.5 * self.sup(i, m) * ()