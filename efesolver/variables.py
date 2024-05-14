import sys

print("Importing Sympy ...", end="")
sys.stdout.flush()
import sympy
print("\rSympy imported successfully.")

axes = sympy.symbols("t x y z")
t, x, y, z = axes
r = sympy.sqrt((x ** 2) + (y ** 2) + (z ** 2))
r2 = (x ** 2) + (y ** 2) + (z ** 2)
r3 = ((x ** 2) + (y ** 2) + (z ** 2)) ** (3/2)
c, G, pi = sympy.symbols("c G pi")
c2 = c ** 2

def newVariable(n: str):
	return sympy.Symbol(n)

def schwarzschild(M): 
	return 1 - (2 * G * M / (r * c2))

def lensethirring():
	return 4 * G / (r3 * c2)