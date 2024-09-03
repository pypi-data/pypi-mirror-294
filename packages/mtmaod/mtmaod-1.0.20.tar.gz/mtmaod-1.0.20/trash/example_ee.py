import numpy as np
import matplotlib.pyplot as plt


def rr(x):
    up_ee = 1.15 * x + 0.05
    down_ee = 0.85 * x - 0.05
    f = lambda x: np.log(x)
    up = f(up_ee)
    if down_ee > 0:
        down = f(down_ee)
    else:
        down = -15
    return up - down


x = np.linspace(0.060, 4, 1000)
y = [rr(i) for i in x]
plt.plot(x, y, label="ee")
plt.show()
