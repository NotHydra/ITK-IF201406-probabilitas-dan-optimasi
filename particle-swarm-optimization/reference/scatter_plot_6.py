import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Create a figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 10)  # Set x-axis limits
ax.set_ylim(0, 10)  # Set y-axis limits

# Create initial scatter plot
scatter = ax.scatter([], [])


# Update function for animation
def update(frame):
    # Generate random data points
    x = np.random.rand(10) * 10  # Random x-coordinates
    y = np.random.rand(10) * 10  # Random y-coordinates

    # Update scatter plot data
    scatter.set_offsets(np.c_[x, y])
    return (scatter,)


# Create animation
ani = FuncAnimation(fig, update, frames=range(100), interval=1000, blit=True)

plt.show()
