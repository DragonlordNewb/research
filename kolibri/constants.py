from math import pi
from decimal import Decimal

pi = Decimal(pi) # circle constant

c = Decimal(299792458) # speed of light
c2 = c ** 2 # c ^ 2
c3 = c ** 3 # c ^ 3
c4 = c ** 4 # c ^ 4

G = Decimal(6.6714e-11) # gravitational constant

alpha = Decimal(7.2973525693e-3) # fine-structure constant
h = Decimal(6.62607015e-34) # planck constant
hc = h * c
hbar = h / 2 * pi # reduced planck constant
hbarc = hbar * c

Qe = Decimal(1.60217663e-19) # charge of an electron
mu0 = (2 * alpha * h) / ((Qe ** 2) * c) # vacuum permeability
epsilon0 = 1 / (mu0 * c2) # vacuum permittivity
ke = 1 / (4 * pi * epsilon0) # Coulomb constant