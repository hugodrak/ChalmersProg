import matplotlib.pyplot as plt

def logmap(r, val):
    return r*val*(1-val)

def experiment(r, x, times):
    for n in range(times):
        print(x)
        x = logmap(r, x)

def table(r, x1, x2, times):
    for n in range(times):
        print(x1, x2)
        x1 = logmap(r, x1)
        x2 = logmap(r, x2)

def attractors(r, x, n, epsilon):
    numbers = []
    found = []
    times = 0
    while times < n:
        match = False
        x = logmap(r, x)
        for i, prev in enumerate(numbers):
            if abs(x-prev) < epsilon:
                if i not in found:
                    found.append(i)
                break
        numbers.append(x)


        times += 1
    return [numbers[i] for i in found]


def bifurcation_diagram(r_max, r_step):
    x_vals = []
    y_vals = []
    for r in range(0, int(r_max//r_step)):
        r = r*r_step
        attracts = attractors(r, 0.15, 300, 1e-5)
        y_vals.extend(attracts)
        x_vals.extend([r for _ in range(len(attracts))])

    plt.scatter(x_vals, y_vals, s=1)
    plt.show()

#experiment(3.9, 0.2, 20)
#table(3.9, 0.2, 0.21, 20)

#attractors(3.5, 0.2, 100, 1e-5)
bifurcation_diagram(4.0, 0.003)
