import matplotlib.pyplot as plt
import math
import numpy as np
data = open("data.txt", 'r').read().splitlines()
n = []
rand = []
p95 = []
sort = []
for x in data:
    s = x.split("|")
    if len(s) > 1:
        s = [i.replace(" ", "") for i in s]
        s = [x if x.isnumeric() else 0 for x in s]
        n.append(int(s[0]))
        rand.append(int(s[2]))
        p95.append(int(s[5]))
        sort.append(int(s[8]))
print(n)
print(rand)
print(p95)
print(sort)
plt.plot(n, rand)
plt.plot(n, p95)
plt.plot(n, sort)
nn = np.asarray(n)
plt.plot(nn, nn)
plt.plot(nn, nn**2)
plt.plot(nn, nn*np.log10(nn))
plt.plot(nn, np.log(nn))
plt.ylim([0, 2e6])
plt.legend(["Random", "95%", "Sorted", "n", "n**2", "n*log(n)", "log(n)"])
plt.show()
