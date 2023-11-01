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

# Prefixes
quetta = Decimal(10) ** 30
ronna = Decimal(10) ** 27
yotta = Decimal(10) ** 24
zeta = Decimal(10) ** 21
exa = Decimal(10) ** 18
peta = Decimal(10) ** 15
tera = Decimal(10) ** 12
giga = Decimal(10) ** 9
mega = Decimal(10) ** 6
kilo = Decimal(10) ** 3
hecto = Decimal(10) ** 2
deca = Decimal(10)
#
deci = Decimal(10) ** -1
centi = Decimal(10) ** -2
milli = Decimal(10) ** -3
micro = Decimal(10) ** -6
nano = Decimal(10) ** -9
pico = Decimal(10) ** -12
femto = Decimal(10) ** -15
atto = Decimal(10) ** -18
zepto = Decimal(10) ** -21
yocto = Decimal(10) ** -24
ronto = Decimal(10) ** -27
quecto = Decimal(10) ** -30