# solve the quadratic formula
import math


def quadr(a, b, c):
    discr = b**2 - 4*a*c
    if discr < 0:
        return []

    rdiscr = math.sqrt(discr)

    res_pos = (-b + rdiscr)/(2*a)
    res_neg = (-b - rdiscr)/(2*a)
    if res_pos == res_neg:
        return [res_pos]
    else:
        return [res_pos, res_neg]


print(quadr(1, 2, 1))
