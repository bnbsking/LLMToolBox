import matplotlib.pyplot as plt
import numpy as np

# Generate x values from 0.0 to 10.0 with a step of 0.02
x = np.arange(0.0, 10.0, 0.02)

# Calculate y values as sine(3*pi*x)
y = np.sin(3 * np.pi * x)

# Create the figure and axes
fig, ax = plt.subplots(figsize=(4, 4))  # Set figure size to 4x4 inches

# Plot the line
ax.plot(x, y)

# Set x-axis and y-axis limits
ax.set_xlim([-2, 10])
ax.set_ylim([-6, 6])

# Display the plot

plt.savefig('/app/agents/text2chart/v1/save/matplotbench_easy/code/9/v1.png'); plt.close()