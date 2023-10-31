from kolibri import *

st = spacetime.Spacetime()
m = metric.Schwarzschild()
st << m

p1 = entity.Particle("p1", Vec3(0, 0, 0), 1, electric=1)
st << p1
p2 = entity.Particle("p2", Vec3(1, 1, 1), 1, electric=-1)
p2.velocity += Vec3(1, 2, 3)
st << p2

f = force.ElectromagneticInteraction()
st << f

print(m.warp(p1.atoms()[0], Vector.zero(4)))

st.trace(1000000, "p1", "p2")