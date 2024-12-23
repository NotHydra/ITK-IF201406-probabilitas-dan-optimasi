import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Create a figure and axis
fig, ax = plt.subplots()
x = np.linspace(0, 2 * np.pi, 100)
(line,) = ax.plot(x, np.sin(x))  # Initial plot


# Function to update the content
def update(frame):
    line.set_ydata(np.sin(x + frame / 10.0))  # Update y-data
    return (line,)


# Create an animation
FuncAnimation(
    fig,  # The figure to animate
    update,  # The function to call at each frame
    frames=range(100),  # The range of frames (0 to 99)
    interval=200,  # Interval in milliseconds between updates
    blit=True,  # Use blitting for better performance
)

plt.show()
