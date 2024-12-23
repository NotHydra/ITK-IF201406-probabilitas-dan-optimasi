import matplotlib.pyplot as plt

# Data
x1 = [1, 2, 3, 4, 5]
y1 = [10, 20, 25, 30, 35]
x2 = [3, 4, 5, 6, 7]
y2 = [30, 40, 50, 60, 70]

# Plot multiple datasets
plt.scatter(x1, y1, color="blue", label="Dataset 1")
plt.scatter(x2, y2, color="green", label="Dataset 2")
plt.title("Scatter Plot with Multiple Datasets")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.show()
