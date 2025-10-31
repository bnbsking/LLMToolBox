import matplotlib.pyplot as plt
import numpy as np

# Generate the numerical sequence
x = np.arange(0.0, 3.0, 0.02)

# Calculate the values for the three lines
y1 = x**2
y2 = np.cos(3*np.pi*x)
y3 = y1 * y2

# Create the plot
plt.plot(x, y1, label='square')
plt.plot(x, y2, label='oscillatory')
plt.plot(x, y3, label='damped')

# Add labels and title
plt.xlabel('time')
plt.ylabel('amplitude')
plt.title('Damped oscillation')

# Add a legend
plt.legend()

# Display the plot

plt.savefig('/app/agents/text2chart/v1/save/matplotbench_easy/code/10/v1.png'); plt.close()