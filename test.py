import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate sample 4D data
np.random.seed(42)
n_points = 1000
x = np.random.rand(n_points)
y = np.random.rand(n_points)
z = np.random.rand(n_points)
f_xyz = np.random.rand(n_points)  # This is the fourth dimension

# Create a 3D scatter plot with color mapping
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(x, y, z, c=f_xyz, cmap='viridis')

# Add color bar
cbar = plt.colorbar(scatter)
cbar.set_label('f(x, y, z)')

# Show the plot
plt.show()