import kolibri

calc = kolibri.Calculus()

l = kolibri.Vector(1, 2, 3)

f1 = lambda v: v.x * v.y * v.z
f2 = lambda v: kolibri.Vector(v.x ** 2, v.y ** 3, v.z / 2)
f3 = lambda v: kolibri.Vector(0, -(v.x ** 2), 0)

print("Gradient of f1 = xyz at", l, "=", calc.gradient(f1, l))
print("Divergence of f2 = x^2i + y^2j + zk/2 at", l, "=", calc.divergence(f2, l))
print("Curl of f3 = -x^2j at", l, "=", calc.curl(f3, l))