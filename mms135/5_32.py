import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def xyz_funct(t, a, w):
    x = a*math.cos(w*t)
    y = a*math.sin(w*t)
    z = a*w*t
    return (x,y,z)


def plot(end_time, a, w):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    times = range(end_time+1)
    xs = []
    ys = []
    zs = []
    for time in times:
        vector = xyz_funct(float(time), float(a), float(w))
        xs.append(vector[0])
        ys.append(vector[1])
        zs.append(vector[2])

    ax.plot(xs, ys, zs)
    fig.show()


plot(100, 0.1, 0.1)
plot(100, 0.1, 0.2)
plot(100, 0.1, 0.4)

