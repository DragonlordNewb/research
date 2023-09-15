from stem1.engine import *

st = Spacetime(ClassicalSchwarzschild(), LinearGravitational())

st.add(
	Particle(energy=10e+9 * constants.c2), 
	position=Vec3(0, 0, 0)
)

st.add(
	Particle(energy=10e+9 * constants.c2), 
	position=Vec3(0, 1, 0), 
	linearVelocity=Vec3(0, -0.001, -0.001)
)

st.mon(
