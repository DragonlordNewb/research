print("Importing Kolibri")
import kolibri

print("Setting up spacetime")

st = kolibri.spacetime.Spacetime()

print("  Adding potential well")

f = kolibri.field.real.PotentialWell(radius=5, depth=10)
st.fields << f

print(" ", f)

print("  Adding particle")

p = kolibri.body.real.Particle("p", kolibri.Vector(0.9, 0.2, 0.5), energy=1)
p.accelerate(kolibri.Vector(1, 2, -0.5))
st.bodies << p
print(" ", p)

print(st)

print("  Assuming Minkowski space")
st.metric = kolibri.metric.real.Minkowski()
print(" ", st.metric)

print("Tracking particle location:")
try:
	while True:
		st.tick(100)
		print(p.location)
except KeyboardInterrupt:
	pass