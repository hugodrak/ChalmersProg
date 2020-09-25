import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("n")
args = parser.parse_args()


def powers(list, start, stop):
    res = []
    for v in list:
        pwrs = [v**p for p in range(start, stop+1)]
        res.append(pwrs)

    return res

def polreg(file, n):
    measurements = np.loadtxt(file)
    x, y = np.transpose(measurements)
    Xp = np.array(powers(x,0,n))
    Yp = np.array(powers(y,1,1))
    Xpt = np.transpose(Xp)
    a = np.matmul(np.linalg.inv(np.matmul(Xpt, Xp)), np.matmul(Xpt, Yp))
    a = a[:,0]
    return a, x, y

def poly(a, x):
    tot = 0
    n = 0
    for koef in a:
        tot += koef*(x**n)
        n+=1
    return tot

if __name__ == "__main__":
    n = int(args.n)
    a, x, y = polreg(args.input, n)
    x_max = int(np.max(x))
    x_min = int(np.min(x))
    temperatures = np.linspace(x_min, x_max, int(abs(x_max-x_min)/0.2)).tolist()
    chirps = []
    for temp in temperatures:
        res = poly(a, temp)
        chirps.append(res)
    plt.plot(x,y, 'ro')
    plt.plot(temperatures, chirps)
    plt.show()
