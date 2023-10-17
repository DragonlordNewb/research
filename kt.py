import kolibri

calc = kolibri.Calculus()

a = kolibri.Vector(1, 2, 3)
b = kolibri.Vector(0, 1, 1)

f1 = lambda v: v.x * v.y * v.z
f2 = lambda v: kolibri.Vector(v.x ** 2, v.y ** 3, v.z / 2)
f3 = lambda v: kolibri.Vector(0, -(v.x ** 2), 0)

print("Gradient of f1 = xyz at", a, "=", calc.gradient(f1, a))
print("Divergence of f2 = x^2i + y^2j + zk/2 at", a, "=", calc.divergence(f2, a))
print("Curl of f3 = -x^2j at", a, "=", calc.curl(f3, a))
print("Integral in f from ", a, "to", b, "=", calc.lineIntegral(f, a, b))