import scipy.integrate as spint
import numpy as np
import matplotlib.pyplot as plt

def f_in(x):
    return 2*x

def model(t, y):
    k = 0.5
    dydt = -k * y
    return dydt

sol = spint.solve_ivp(model, [0, 10], [1], method="Radau")

print(sol.t)
print(sol.y)
plt.plot(sol.t, sol.y[0])
plt.xlabel('time')
plt.ylabel('y(t)')
plt.show()

#
# print(sorted(dir(scipy)))
# ivp_solver = scipy.integrate.solve_ivp()
