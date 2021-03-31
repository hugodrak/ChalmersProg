import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation

# Grupp 13

a = 4
b = 10

w0 = 3
init = [0.5, 0]
g = 9.81

duration = 15


def f(xi):
    return a * np.sin(xi) ** 2 + b * xi ** 2


def f_prim(y1):
    return 2 * (a * np.sin(2 * y1) + b * y1)


def f_bis(y1):
    return 2 * (a * np.cos(2 * y1) ** 2 + b)


def func(t, y):
    y1 = y[0]
    y2 = y[1]

    result = np.array([

        y2,

        # (B-C-D)/A
        (w0 ** 2 * y1 - f_prim(y1) * f_bis(y1) * y2 ** 2 - g * f_prim(y1))
        / (f_prim(y1) ** 2 + 1)
    ])

    return result


sol = solve_ivp(func, [0, duration], init, method="Radau", t_eval=np.linspace(0, duration, 10000))

z = f(sol.y[0])  # f(xi),

xi = sol.y[0, :]
t = sol.t
# Convert to xyz-coords
x = xi * np.cos(w0 * t)
y = xi * np.sin(w0 * t)

# Remove comment for 2D plot
# plt.plot(sol.t, sol.y[0, :])
# plt.show()
# import sys;
# sys.exit()

fig = plt.figure("X,Y,Z")
_3d_plot = fig.add_subplot(111, projection='3d')
_3d_plot.plot(x, y, z)

_3d_plot.set_xlabel('X')
_3d_plot.set_ylabel('Y')
_3d_plot.set_zlabel('Z')
_3d_plot.set_zlim(0.0, 3.5)
_3d_plot.set_title(f'w0: {w0:0.5f}')

plt.show()
