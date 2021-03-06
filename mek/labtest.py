import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt

def f(t,xi):
    xi_prim = 2*xi
    return xi_prim

# initial condition
y0=[0.5]

# stop time
tend=10

sol = scipy.integrate.solve_ivp(f,
                                [0,tend],
                                y0,
                                method='Radau',
                                t_eval=np.linspace(0,tend,10000))

plt.plot(sol.t,sol.y[0,:])
plt.xlabel('time')
plt.ylabel('eta(t)')
plt.show()