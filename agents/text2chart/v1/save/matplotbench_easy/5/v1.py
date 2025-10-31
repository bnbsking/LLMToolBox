import matplotlib.pyplot as plt

# Data for the pie chart
fruits = ['Apples', 'Oranges', 'Bananas']
proportions = [35, 45, 20]

# Create the pie chart
plt.pie(proportions, labels=fruits, autopct='%1.1f%%', startangle=90)

# Add a title to the chart
plt.title('Fruit Distribution in a Basket')

# Ensure the circle's proportion
plt.axis('equal')


plt.savefig('/app/agents/text2chart/v1/save/matplotbench_easy/code/5/v1.png'); plt.close()