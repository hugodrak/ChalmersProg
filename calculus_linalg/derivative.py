

equation = "2*x^3+3*x"

new = ""
done = False
while not done:
    i = equation.find("x")
    if i == -1:
        done = True
    if equation[i+1] == "^":
        ex = int(equation[i+2])
        new += str(int(equation[i-2])*ex)+"*x"+(f"^{ex-1}" if ex-1 != 1 else "")
        equation = equation[i+2:]
    h=0
