import matplotlib
import json
import matplotlib.pyplot as plt

#fake data to create visualizations that will be replaced once there are calculations
y = ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
d1 = [33, 34, 35, 36, 38, 39, 19, 21, 28, 36, 34]

fig, ax = plt.subplots()
ax.plot(y, d1)
ax.set_xlabel("Year")
ax.set_ylabel("Domestic flights taken (in mil)")
ax.set_title("Number of domestic flights taken yearly")
ax.grid()

fig.savefig("fake_airplane_data.png")
plt.show()

N = 12
width = 0.35
ind = np.arange(N)

p1 = ax.bar(ind, total, width, color='blue')
p2 = ax.bar()

