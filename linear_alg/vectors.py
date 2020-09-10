import numpy as np


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

    return ans, f"{i}i{j if j<0 else '+'+str(j)}j{k if k<0 else '+'+str(k)}k"


print(cross_product((2,-1,2), (-1,-2,1)))








