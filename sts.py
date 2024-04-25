from spacetimeengine import *

import warnings
warnings.simplefilter("ignore")

index_config = "dd"
G, R, c = symbols('G R c')
tau = symbols('tau')
x0 = Symbol('t')
x1 = Symbol('x')
x2 = Symbol('y')
x3 = Symbol('z')
r = sqrt((x1**2)+(x2**2)+(x3**2))
coordinate_set = [x0, x1, x2, x3]
cosmological_constant = 0
metric = Matrix([    
					[ 1+((tanh(r-R)-tanh(r+R)))/2, 0, 0, 0 ],
					[ 0,                      -1, 0, 0 ],
					[ 0,                       0, -1, 0],
					[0, 0, 0, -1]
				])

# An array detailing the solution.
solution_array = [ metric, coordinate_set, index_config, cosmological_constant ]
print("Solving for stress-energy tensor ...")
st = SpaceTime(solution_array,True)
print(st.stress_energy_tensor_uu)