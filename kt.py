import kolibri

st = kolibri.spacetime.Spacetime()
st.metric = kolibri.metric.real.Minkowski()

p = kolibri.body.real.Particle("p", kolibri.Vector(0, 0, 0))
p.accelerate(kolibri.Vector(1, 2, 3))
st.bodies << p

print("Before:", p)
st.tick(iterations=1000000)
print("After:", p)
