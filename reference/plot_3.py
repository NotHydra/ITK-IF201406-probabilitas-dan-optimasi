import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Initialize the figure and axis
fig, ax = plt.subplots()
ax.set_title("Dynamic Plot with Multiple Datasets")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")

# Create empty lines for the datasets
(line1,) = ax.plot([], [], label="Dataset 1", color="blue")
(line2,) = ax.plot([], [], label="Dataset 2", color="green")

# Add a legend
ax.legend()

# Set axis limits
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)


# Generate dynamic data
def generate_data():
    """Simulates dynamic datasets."""
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x + np.random.random())
    y2 = np.cos(x + np.random.random())
    return x, y1, y2


# Update function for animation
def update(frame):
    """Updates the plot with new data."""
    x, y1, y2 = generate_data()
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2


# Create the animation
ani = FuncAnimation(
    fig, update, interval=2000
)  # Update every 2000 milliseconds (2 seconds)

# Show the plot
plt.show()
