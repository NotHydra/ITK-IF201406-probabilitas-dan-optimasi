import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Data
x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 35]
z = [100, 200, 300, 400, 500]

# 3D Scatter Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(x, y, z, c="red", marker="o")

ax.set_title("3D Scatter Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")

plt.show()
