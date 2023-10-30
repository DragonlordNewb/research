from kolibri import *

st = spacetime.Spacetime()
m = metric.Minkowski()
st << m
p = entity.Particle(Vec3(0, 0, 0), 1)
st << p
p.velocity += Vec3(1, 1, 1)
print(p.location)
st.tick(1000)
print(p.location)