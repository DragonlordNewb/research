from kolibri import *

st = spacetime.Spacetime(0.000001)
m = metric.Schwarzschild()
st << m

p1 = entity.Particle("p1", Vec3(1, 1, 1), 1, electric=1e-6)
p1.velocity += Vector(0, 0, 1e-3)
st << p1
p2 = entity.Particle("p2", Vec3(0, 0, 0), 1000000, electric=-1e-6)
st << p2

f = force.ElectromagneticField()
st << f

st.trace("p1", 10000000)