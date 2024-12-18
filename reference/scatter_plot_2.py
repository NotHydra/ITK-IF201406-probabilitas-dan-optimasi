import matplotlib.pyplot as plt

# Data
x = [5, 7, 8, 7, 2, 17, 2, 9, 4, 11]
y = [99, 86, 87, 88, 100, 86, 103, 87, 94, 78]
colors = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # Color gradient
sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]  # Point sizes

# Plot
plt.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap="viridis")
plt.colorbar(label="Color Scale")
plt.title("Scatter Plot with Color and Size")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
