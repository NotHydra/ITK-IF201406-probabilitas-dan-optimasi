import matplotlib.pyplot as plt

# Coordinates of two points
x = [1, 4]  # X-coordinates
y = [2, 8]  # Y-coordinates

# Scatter plot for the dots
plt.scatter(x, y, color="blue", label="Dots")

# Line connecting the dots
plt.plot(x, y, color="red", linestyle="--", label="Connecting Line")

# Adding an arrow
plt.annotate(
    "",  # No text
    xy=(x[1], y[1]),  # End point of the arrow
    xytext=(x[0], y[0]),  # Start point of the arrow
    arrowprops=dict(arrowstyle="->", color="green", lw=2),  # Arrow style
)

# Adding labels and legend
plt.title("Scatter Plot with Line and Arrow")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()

plt.show()
