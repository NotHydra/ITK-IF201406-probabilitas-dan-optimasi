import matplotlib.pyplot as plt

# Sample datasets
x1 = [1, 2, 3, 4, 5]
y1 = [5, 4, 3, 2, 1]

x2 = [1, 2, 3, 4, 5]
y2 = [1, 2, 3, 4, 5]

x3 = [1, 2, 3, 4, 5]
y3 = [2, 3, 4, 5, 6]

# Create scatter plots for each dataset
plt.scatter(x1, y1, color="r", label="Dataset 1")
plt.scatter(x2, y2, color="g", label="Dataset 2")
plt.scatter(x3, y3, color="b", label="Dataset 3")

# Add labels and title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Multiple Datasets on Scatter Plot")

# Show legend
plt.legend()

# Display the plot
plt.show()
