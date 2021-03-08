from sympy.solvers import solvers
from sympy import Symbol
import sympy

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

print(solvers.solve([x + y + 5, y + z], x))

print(sympy.simplify(x + y == 4))
