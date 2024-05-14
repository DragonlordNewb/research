import sys 

from efesolver import variables
from efesolver.variables import sympy

class Metric:

	def __init__(self, g0mu, g1mu, g2mu, g3mu, cacheEverything=True, quiet=False):
		self.lower = sympy.Matrix([g0mu, g1mu, g2mu, g3mu])
		self.upper = self.lower.inv()

		self.cachedChristoffelSymbols = [[[None] * 4] * 4] * 4
		self.cachedRicciComponents = [[None] * 4] * 4
		self.scalarCurvature = None

		if cacheEverything:
			for i in range(4):
				for k in range(4):
					for l in range(4):
						self.christoffel(i, k, l, quiet)
			for i in range(4):
				for j in range(4):
					self.ricci(i, j, quiet)
			self.scalar(quiet)

	def sub(self, mu, nu):
		return self.lower[mu, nu]

	def sup(self, alpha, beta):
		return self.upper[alpha, beta]

	def christoffel(self, i, k, l, quiet=False):
		if self.cachedChristoffelSymbols[i][k][l] is not None:
			if not quiet:
				print("Found cached Christoffel symbol (ikl = " + str(i) + str(k) + str(l) + ").")
			return self.cachedChristoffelSymbols[i][k][l]
		else:
			if not quiet:
				print("Computing Christoffel symbol (ikl = " + str(i) + str(k) + str(l) + ")...", end="")
			sys.stdout.flush()
			s = 0
			for m in range(4):
				s += 0.5 * self.sup(i, m) * (
					sympy.diff(self.sub(m, k), variables.axes[l])
				  + sympy.diff(self.sub(m, l), variables.axes[k])
				  + sympy.diff(self.sub(k, l), variables.axes[m])
				)
			if not quiet:
				print("\rSuccessfully computed Christoffel symbol (ikl = " + str(i) + str(k) + str(l) + ").")
			self.cachedChristoffelSymbols[i][k][l] = s
			return s
		
	def ricci(self, i, j, quiet=False):
		if self.cachedRicciComponents[i][j] is not None:
			if not quiet:
				print("Found cached Ricci tensor component (ij = " + str(i) + str(j) + ").")
			return self.cachedRicciComponents[i][j]
		else:
			if not quiet:
				print("Computing Ricci tensor component (ij = " + str(i) + str(j) + ")...", end="")
			s = 0
			for k in range(4):
				for m in range(4):
					s += sympy.diff(self.christoffel(k, i, j, True), variables.axes[k]) \
					+ sympy.diff(self.christoffel(k, i, k, True), variables.axes[j]) \
					+ (self.christoffel(k, i, j, True) * self.christoffel(m, k, m, True)) \
					+ (self.christoffel(k, i, m, True) * self.christoffel(m, j, k, True))
			if not quiet:
				print("\rSuccessfully computed Ricci tensor component. (ij = " + str(i) + str(j) + ")")
			self.cachedRicciComponents[i][j] = s
			return s
		
	def scalar(self, quiet=False):
		if self.scalarCurvature is not None:
			if not quiet:
				print("Found cached scalar curvature")
			return self.scalarCurvature
		else:
			if not quiet:
				print("Computing scalar curvature ...", end="")
			s = 0
			for i in range(4):
				for j in range(4):
					s += self.sup(i, j) * self.ricci(i, j, True)
			print("\rSuccessfully computed scalar curvature.")
			self.scalarCurvature = s
			return s