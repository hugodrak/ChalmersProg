## Do upper and lower reiman sum


n = 4
p = [1,2]
steps = [((p[1]-p[0])/n)*(i+1)+p[0] for i in range(n-1)]
print(steps)

summ = 0
for step in steps:
    summ += 1/step

lower = (1/n)*(summ+(1/p[1]))
print(lower)
upper = (1/n)*(summ+(1/p[0]))
print(upper)
