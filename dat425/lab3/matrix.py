

def transpose(matrix):
    if not matrix:
        return []
    new_matrix = []
    for i in range(len(matrix[0])):
        new_matrix.append([])
        for r in range(len(matrix)):
            new_matrix[i].append(matrix[r][i])

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
    lines = open(file, "r").read().splitlines()
    matrix = []
    for line in lines:
        ls = line.split("\t")
        if len(ls) == 2:
            matrix.append([float(ls[0]), float(ls[1])])
    return matrix
