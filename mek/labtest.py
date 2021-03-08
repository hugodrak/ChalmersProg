import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt
import math

def f(t,xi):

    xi_prim2 = -0.5*xi
    xi_prim = np.array([-np.exp(-t)])
    return xi_prim

# initial condition
y0=[1.0]

# stop time
tend=5

sol = scipy.integrate.solve_ivp(f,
                                [0, tend],
                                y0,
                                method='Radau',
                                t_eval=np.linspace(0,tend,10000))

plt.plot(sol.t,sol.y[0,:])
plt.xlabel('time')
plt.ylabel('eta(t)')
plt.show()