import numpy as np
matrix = [[5,10,15],[15,20,25],[25,30,35]]

def float_range(f_range, step):
    fl = []
    n = f_range[0]
    while n < f_range[1]+step:
        fl.append(n)
        n += step
    return fl



class Matrix:
    def __init__(self, matrix, floats=False):
        self.matrix = matrix
        self.all_int = self.check_int()
        if self.all_int and not floats:
            self.to_int()
        self.polys_row = {}
        self.polys_col = {}

    def col_poly(self, col_i):
        if col_i in self.polys_col.keys():
            return self.polys_col[col_i]
        else:
            col_vals = []
            for r in range(len(matrix)):
                col_vals.append(matrix[r][col_i])
            func = self.find_poly(col_vals)
            self.polys_col[col_i] = func
            return func

    def row_poly(self, row_i):
        if row_i in self.polys_row.keys():
            return self.polys_row[row_i]
        else:
            func = self.find_poly(self.matrix[row_i])
            self.polys_row[row_i] = func
            return func

    def get(self, row, col):
        if type(row) == int and type(col) == int:
            return self.matrix[row][col]

        elif type(row) == float and type(col) == int:
            return round(self.calc_poly(self.col_poly(col), row), 2)

        elif type(row) == int and type(col) == float:
            return round(self.calc_poly(self.row_poly(row), col), 2)

        elif type(row) == float and type(col) == float:
            col_values = [self.calc_poly(self.find_poly(self.matrix[ri]), col) for ri in range(len(matrix))]

            col_func = self.find_poly(col_values)
            est = self.calc_poly(col_func, row)

            return round(est, 2)

    def find_poly(self, row, degree=2):
        indexes = range(len(row))
        func = np.polyfit(indexes, row, degree)
        return func

    def calc_poly(self, func, x):
        a, b, c = func
        return a*(x**2)+b*x+c

    def pp_poly(self, row_i):
        a, b, c = self.polys[row_i]
        print(f"{a}x²+{b}x+{c}")

    def pp(self):
        for row in self.matrix:
            tot = ""
            for col in row:
                tot += str(round(col, 1)).rjust(5)
            print("|"+tot+"|")

    def range(self, row_range, row_step, col_range, col_step):
        new_matrix = []
        ri = 0
        for r_f in float_range(row_range, row_step):
            new_matrix.append([])
            for c_f in float_range(col_range, col_step):
                new_matrix[ri].append(self.get(r_f, c_f))
            ri += 1
        return Matrix(new_matrix)

    def check_int(self):
        all_int = True
        for row in self.matrix:
            for col in row:
                if abs(col - int(col)) > 1e-8:
                    all_int = False
        return all_int

    def to_int(self):
        cols = len(self.matrix[0])
        for r in range(len(self.matrix)):
            for c in range(cols):
                val = self.matrix[r][c]
                self.matrix[r][c] = int(val)

    def mid(self):
        # TODO: implement this to get the element in the middle of the matrix
        pass

m = Matrix(matrix)
m.pp()
#print(m.get(0, 0.5))
#print(m.get(0.5, 0))
#print(m.get(0.5, 0.5))
nm = m.range([.0, 1.0], .25, [.0, 1.], .25).pp()
