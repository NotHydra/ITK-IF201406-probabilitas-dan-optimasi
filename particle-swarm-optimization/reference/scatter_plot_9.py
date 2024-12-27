import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Coordinates of points
x = [1, 4, 8]  # X-coordinates
y = [2, 8, 12]  # Y-coordinates

# Create a figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 15)

# Scatter plot for the dots
ax.scatter(x, y, color="blue", label="Dots")

# Initial arrow (invisible at the start)
arrow = ax.annotate(
    "",  # No text
    xy=(0, 0),
    xytext=(0, 0),
    arrowprops=dict(arrowstyle="->", color="black", lw=2),
)

# Adding labels and legend
ax.set_title("Scatter Plot with Animated Arrow")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.legend()


# Update function for animation
def update(frame):
    start_idx = frame % (len(x) - 1)  # Loop through points
    end_idx = start_idx + 1
    arrow.set_position((x[start_idx], y[start_idx]))
    arrow.xy = (x[end_idx], y[end_idx])
    arrow.xytext = (x[start_idx], y[start_idx])


# Create animation
ani = animation.FuncAnimation(
    fig, update, frames=len(x) - 1, interval=1000, repeat=True
)

# Display animation
plt.show()
