from kolibri import *

st = spacetime.Spacetime(0.000001)
m = metric.Schwarzschild()
st << m

p1 = entity.Particle("p1", Vec3(0, 0, 0), 1, electric=1e-9)
st << p1
p2 = entity.Particle("p2", Vec3(1, 1, 1), 1, electric=-1e-8)
st << p2
p3 = entity.Particle("p3", Vec3(-1, 2, 0), 1, electric=1e-9)

f = force.ElectromagneticInteraction()
st << f

print(m.warp(p1.atoms()[0], Vector.zero(4)))

st.trace("p1", 10000000)