# Advanced SpaceTime Engineering Research software realism component.
# Adds various real metrics and constants to the Universe.

from aster.engine import Metric

# Various real physical constants.

# Constants are labelled "exact" when, by definition, the constant
# holds the exact value specified, and labelled "not exact" when
# the value given is only a close approximation to within a few
# decimal places.

F = 96485.3321 # Faraday constant - exact
NA = 6.02214076e+23 # Avogadro's number - exact
h = 6.62607015e-34 # Planck constant - exact
Qe = F / NA # Elementary charge - exact
alpha = 7.2973525693e-3 # Fine-structure constant, a.k.a. ~1/137 - not exact
c = 299792458 # Speed of light in a vacuum - exact
c2 = c ** 2 # c^2 - useful for saving a bit of computation time
G = 6.6743e-11 # Gravitational constant - not exact
mu0 = (2 * alpha * h) / ((Qe ** 2) * c) # Vacuum permeability - not exact
epsilon0 = 1 / (mu0 * c2) # Vacuum permittivity - not exact

# SI prefixes, for fun mostly
quetta = 10 ** 30
ronna = 10 ** 27
yotta = 10 ** 24
zetta = 10 ** 21
exa = 10 ** 18
peta = 10 ** 15
tera = 10 ** 12
giga = 10 ** 9
mega = 10 ** 6
kilo = 10 ** 3

milli = 10 ** -3
micro = 10 ** -6
nano = 10 ** -9
pico = 10 ** -12
femto = 10 ** -15
atto = 10 ** -18
zepto = 10 ** -21
yocto = 10 ** -24
ronto = 10 ** -27
quecto = 10 ** -30

@Metric.register
class Minkowski(Metric):

	"""
	In Minkowski space (which is perfectly flat), space and time are
	constant.
	"""

	def spaceContraction(self, location):
		return 1

	def timeDilation(self, location):
		return 1
