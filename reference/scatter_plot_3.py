import matplotlib.pyplot as plt

# Data
x = [5, 7, 8, 7, 2, 17, 2, 9, 4, 11]
y = [99, 86, 87, 88, 100, 86, 103, 87, 94, 78]

# Plot with a custom marker
plt.scatter(x, y, marker="*", color="red", s=200)
plt.title("Scatter Plot with Custom Markers")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
