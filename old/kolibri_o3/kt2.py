from kolibri import *

st = spacetime.Spacetime(0.000001)
m = metric.EinsteinThirringLense()
st << m

p1 = entity.Particle("p1", Vec3(-1, -1, 0), 1)
p1.velocity += Vec3(0.001, 0, 0)
st << p1
p2 = entity.Particle("p2", Vec3(0, 0, 0), 1e+18)
p2.spin += Vector(0, 0, -1000000000)
st << p2

st.trace("p1", 2000001)