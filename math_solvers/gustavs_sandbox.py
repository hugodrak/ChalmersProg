import sympy

alpha, Ffb, Ffa, m, g, Na, Nb, u, m0 = sympy.symbols('alpha Ffb Ffa m g Na Nb u m0')

solution = sympy.solve([
    Ffb - m * g / 2,
    Ffb - u * Nb,
    Na * sympy.cos(alpha) + Ffa * sympy.sin(alpha) - m0 * g - Ffb,
    Na * sympy.sin(alpha) - Ffa * sympy.cos(alpha) - Nb,
    Ffa - Ffb,

], Ffb, Ffa, Na, Nb, m)

for variable, result in solution.items():
    print(f'{variable}: {result}')
