from kolibri import *

st = spacetime.Spacetime(0.000001)
m = metric.Schwarzschild()
st << m

p1 = entity.Particle("p1", Vec3(0, 0, 0), 1, electric=1e-12)
st << p1
p1.velocity += Vec3(-1, 2, 3)
p2 = entity.Particle("p2", Vec3(1, 1, 1), 1, electric=-1e-12)
p2.velocity += Vec3(1, 2, 3)
st << p2

f = force.ElectromagneticInteraction()
st << f

print(m.warp(p1.atoms()[0], Vector.zero(4)))

st.trace("p1", 1000000)