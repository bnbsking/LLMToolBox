import matplotlib.pyplot as plt

# Data for the pie chart
labels = ['Apples', 'Oranges', 'Bananas']
sizes = [35, 45, 20]
colors = ['red', 'orange', 'yellow']  # Optional: Customize colors

# Create the pie chart
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

# Add a title
plt.title('Fruit Distribution in a Basket')

# Ensure the circle's proportion
plt.axis('equal')

plt.savefig('/app/agents/text2chart/v1/save/matplotbench_easy/code/5.png'); plt.close()