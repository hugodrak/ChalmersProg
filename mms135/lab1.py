import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

## initial values for group 6: a=5, b=6

# & is xi
# example: 7&'' + 4&' - 5& = 9
# &'' = f(t, &', &)
# but we want: y' = f(t, y) a first order diffeq
# to reduce we introduce & = y_1
# and &' = y_2
# gives us: y'_1 = y_2 = f(t, Y)
# where Y = |y_1, y_2|
# the second is harder but we know that y'_2 = &''
# gives: y'_2 = (-4/7)*y_2 + (5/7)*y_1 + (9/7) = f(t, Y)
# this produces: [y'_1, y'_2] = [y_2, (-4/7)*y_2 + (5/7)*y_1 + (9/7)] = F(t, Y)
# where F(t, Y) is whats goes to solve ivp
global a, b, w0, g
a = 5
b = 6
w0 = 3.0 # 3.0
g = 9.81


# x = xi
def f(x):
    func = a*(np.sin(x)**2) + b*(x**2)
    return func


def fp(x):
    func = a*(np.sin(2*x)) + 2*b*x
    return func


def fpp(x):
    func = 2*a*(np.cos(2*x)) + 2*b
    return func


def H(t, Y):
    y1 = Y[0]
    y2 = Y[1]

    # Y[0] == y1, Y[1] = y2
    func = ((w0**2)*Y[0] - fp(Y[0])*fpp(Y[0])*(Y[1]**2) - fp(Y[0])*g) / (fp(Y[0])**2 + 1)

    return [Y[1], func]


def solver(plot):
    # initial cond
    # xi and xi'
    xi0 = [0.5, 0]

    # time end
    tend = 10

    sol = solve_ivp(H, [0, tend], xi0, method='Radau', t_eval=np.linspace(0, tend, 10000))

    # calculate pos in fixed coordinate system
    xs = []
    ys = []
    zs = sol.y[0]  # f(xi)
    for i, t in enumerate(sol.t):
        xi = sol.y[1][i]
        x = xi * np.cos(w0 * t)
        y = xi * np.sin(w0 * t)
        xs.append(x)
        ys.append(y)


    if plot:
        # 2D
        plt.figure()
        plt.plot(sol.t, sol.y[0,:])
        plt.xlabel("time", fontsize=20)
        plt.ylabel(r"$ \xi(t)$", fontsize=20)
        plt.title(f'w0: {w0}', fontsize=18, fontweight='bold')

        # 3D

        fig = plt.figure()
        three_D = fig.add_subplot(111, projection='3d')
        three_D.plot(xs, ys, zs)

        three_D.set_xlabel('$X$', fontsize=20)
        three_D.set_ylabel('$Y$', fontsize=20)
        three_D.zaxis.set_rotate_label(False)
        three_D.set_zlabel('$Z$', fontsize=20)
        three_D.set_title(f'w0: {w0}', fontsize=18, fontweight='bold')

        plt.show()


solver(plot=True)

# for w in range(14150, 14160, 1):
#     w0 = w/1000
#     solver(plot=True)