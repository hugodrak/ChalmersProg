

def gauss_elimination(matrix_and_sum, row_from, row_to, factor):
    matrix = matrix_and_sum[0]
    sums = matrix_and_sum[1]
    for i in range(len(matrix[0])):
        val_from = matrix[row_from][i]
        matrix[row_to][i] += val_from*factor
        sums[row_to] += sums[row_from]*factor


matrix = [[1,-2,0,-3],
          [0,1,0,-4],
          []]

