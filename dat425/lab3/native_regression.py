import argparse
from matrix import *
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()

def linreg(file):
    measurements = loadtxt(file)
    x, y = transpose(measurements)
    Xp = powers(x,0,1)
    Yp = powers(y,1,1)
    Xpt = transpose(Xp)
    b_m = matmul(invert(matmul(Xpt, Xp)), matmul(Xpt, Yp))
    b = b_m[0][0]
    m = b_m[1][0]
    return b,m,x,y


def pred(b, m, val):
    return b + m * val

if __name__ == "__main__":
    b, m, x, y = linreg(args.input)
    temperatures = list(range(0, 100))
    chirps = []
    for temp in temperatures:
        res = pred(b, m, temp)
        chirps.append(res)

    plt.plot(temperatures, chirps)
    plt.plot(x,y, 'ro')
    plt.show()
