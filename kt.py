import kolibri
st = kolibri.spacetime.Spacetime(resolution=0.000001)
st.metric = kolibri.metric.real.Minkowski()
p = kolibri.body.real.Particle("p", kolibri.Vector(0, 0, 0))
p.accelerate(kolibri.Vector(1, 0, 0))
st.bodies << p

print(p)
for _ in range(10):
	st.tick(iterations=100000)
	print(p)
