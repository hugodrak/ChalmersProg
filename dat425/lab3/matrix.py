
def transpose(matrix):
    old_size = len(matrix), len(matrix[0])
    new_size = old_size[1], old_size[0]
    new_matrix = []
    flat = []
    for row in matrix:
        for col in row:
            flat.append(col)

    i = 0
    for r in range(new_size[0]):
        new_matrix.append([])
        for _ in range(new_size[1]):
            new_matrix[r].append(flat[i])
            i += 1

    return new_matrix


def powers(list, start, stop):
    res = []
    for v in list:
        pwrs = [v**p for p in range(start, stop+1)]
        res.append(pwrs)

    return res


def matmul(mat1, mat2):
    res = []
    for r in range(len(mat1)):
        res.append([])
        row = mat1[r]
        for c in range(len(mat2[0])):
            col = [mat2[i][c] for i in range(len(mat2))]
            tot = 0
            for i in range(len(row)):
                tot += (row[i]*col[i])
            res[r].append(tot)

    return res


def invert(matrix):
    a=matrix[0][0]
    b=matrix[0][1]
    c=matrix[1][0]
    d=matrix[1][1]
    det = (a*d) - (b*c)
    return [[d/det, -b/det], [-c/det, a/det]]


def loadtxt(file):
    pass  # TODO: implement
