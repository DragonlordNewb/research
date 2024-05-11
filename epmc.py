print("loading packages ...", end="")
import sympy
from sympy import *
from einsteinpy.symbolic import EinsteinTensor, MetricTensor

print("done.\ninitializing printing and symbols ...", end="")
sympy.init_printing()

syms = sympy.symbols("t x y z")
consts = sympy.symbols("c G M")
ams = sympy.symbols("Lx, Ly, Lz")
t, x, y, z = syms
c, G, M = consts
Lx, Ly, Lz = ams
r = sqrt((x ** 2) + (y ** 2) + (z ** 2))
FS = 1 - (2 * G * M / (r * (c ** 2)))
FSi = 1 / FS
FLT = 4 * G / ((c ** 2) * (r ** 3))
print("done.\nloading Lense-Thirring metric ...", end="")
m = [
	[(c ** 2) * FS, FLT * Ly * z , FLT * Lz * x, FLT * Lx * y],
	[-1 * FLT * Lz * y, -1 * FSi, 0, 0],
	[-1 * FLT * Lx * z, 0, -1 * FSi, 0],
	[-1 * FLT * Ly * x, 0, 0, -1 * FSi]
]
metric = MetricTensor(m, syms)
print("done.\ncalculating covariant Einstein tensor ...", end="")

einstll = EinsteinTensor.from_metric(metric)
print(einstll.tensor())

print("raising indices ...", end="")
einstuu = einstll.change_config("uu")
print(einstuu.tensor())