import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt
import math


def f(t, z):
    z1 = z[0]
    z2 = z[1]

    result = np.array([
        z2,
        -4 / 7 * z2 + 5 / 7 * z1 + 9 / 7

    ])

    return result



# initial condition
z0 = [1.5, 0]

# stop time
tend = 5

sol = scipy.integrate.solve_ivp(f,
                                [0, tend],
                                z0,
                                method='Radau',
                                t_eval=np.linspace(0, tend, 10000))

plt.plot(sol.t, sol.y[0, :])
plt.xlabel('time')
plt.ylabel('eta(t)')
plt.show()
