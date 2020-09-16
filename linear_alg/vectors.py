import numpy as np
import math


def matrix_sum(matrix):
    # sum 2x2 matrix
    mat_sum = (matrix[0][0]*matrix[1][1])-(matrix[0][1]*matrix[1][0])
    return mat_sum


def cross_product(p1, p2, scalar=None):
    matrix = np.zeros((3, 3))
    if scalar:
        matrix[0] = scalar
    else:
        matrix[0] = (1, 1, 1)

    matrix[1] = p1
    matrix[2] = p2

    i_matrix = np.zeros((2, 2))
    i_matrix[0] = matrix[1][1:3]
    i_matrix[1] = matrix[2][1:3]

    j_matrix = np.zeros((2, 2))
    j_matrix[0] = [matrix[1][0], matrix[1][2]]
    j_matrix[1] = [matrix[2][0], matrix[2][2]]

    k_matrix = np.zeros((2, 2))
    k_matrix[0] = matrix[1][0:2]
    k_matrix[1] = matrix[2][0:2]

    i = matrix[0][0]*matrix_sum(i_matrix)
    j = matrix[0][1]*matrix_sum(j_matrix)
    k = matrix[0][2]*matrix_sum(k_matrix)

    ans = i - j + k
    if i.is_integer():
        i = int(i)
    if j.is_integer():
        j = int(j)
    if k.is_integer():
        k = int(k)

    return {"sum": ans, "text": f"{i}i{j if j<0 else '+'+str(j)}j{k if k<0 else '+'+str(k)}k", "expr": {"i": i, "j": j, "k": k}}


def expr_len(expr):
    return math.sqrt(expr["i"]**2 + expr["j"]**2 + expr["k"]**2)


# find_square root answer
def sqrt_ans(num):
    square = num**2
    if abs(square - int(square)) < 1/1e8:
        square = int(square)
        for i in range(1, 100):
            seek_factor = math.sqrt(square/i)
            if seek_factor.is_integer():
                factor = int(seek_factor)
                return f"{factor}√{i}"

    return f"√{square}"


# scalar = -5, -4, 6
# p1 = -5, -2, 4
# p2 = -4, -1, 0
# prod = cross_product(p1, p2)
# print(prod)
# print(expr_len(prod["expr"])*(1/2))

# scalar = -1,5,-3
# p1 = -4,-4,4
# p2 = 4,-2,-5
# prod = cross_product(p1, p2)
# print(prod)
# print(expr_len(prod["expr"])*(1/2))

# length = expr_len({"i": 7, "j": 8, "k": -5})
# print(round(length, 4), sqrt_ans(length))

p1 = -3,0,-7
p2 = 1,-5,1
prod = cross_product(p1, p2)
print(prod)