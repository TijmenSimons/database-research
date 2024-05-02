from matplotlib import pyplot as plt
import matplotlib.colors as mcolors


x_axis = [10, 100, 1000, 10000, 100000]
x_axis = ["1", 2, 3, 4, 5]



def amplify(line: list[int]) -> list[int]:
    new_line = line
    for idx, point in enumerate(line):
        cur = int(f"1{'0'*(idx+1)}")
        new_line[idx] = point / cur * 1000
    return new_line


# Write
# Redis = [0.01, 0.04, 0.35, 3.58, 35.09]
# Etcd = [0.67, 0.77, 2.19, 17.57, 158.51]
# Aspike = [0.64, 0.67, 1.12, 3.95, 33.59]
# Arango = [0.03, 0.12, 1.09, 10.03, 100.01]
# Orient = [0.38, 0.45, 1.04, 6.79, 64.59]

# Read
Redis  = [0.01, 0.03, 0.31, 3.03, 30.50]
Etcd   = [0.01, 0.10, 0.91, 8.96, 89.53]
Aspike = [0.01, 0.03, 0.28, 2.75, 27.62]
Arango = [0.02, 0.10, 0.92, 9.07, 90.28]
Orient = [0.04, 0.09, 0.60, 6.07, 58.97]


plt.plot(x_axis, amplify(Redis), color=mcolors.TABLEAU_COLORS["tab:blue"])
plt.plot(x_axis, amplify(Etcd), color=mcolors.TABLEAU_COLORS["tab:orange"])
plt.plot(x_axis, amplify(Aspike), color=mcolors.TABLEAU_COLORS["tab:green"])
plt.plot(x_axis, amplify(Arango), color=mcolors.TABLEAU_COLORS["tab:red"])
plt.plot(x_axis, amplify(Orient), color=mcolors.TABLEAU_COLORS["tab:purple"])

plt.xlabel("Test")
plt.ylabel("Tijd in milliseconden")

plt.legend(
    [
        "Redis",
        "Etcd",
        "Aspike",
        "Arango",
        "Orient",
    ]
)
plt.show()
