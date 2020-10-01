from ratio import *
import sys

if len(sys.argv) == 3:
    a_raw = sys.argv[1].split("/")
    b_raw = sys.argv[2].split("/")
    a = Ratio(int(a_raw[0]), int(a_raw[1]))
    b = Ratio(int(b_raw[0]), int(b_raw[1]))

else:
    a = Ratio(2,4)
    b = Ratio(1, 2)

print('a:', a, 'b:', b)
print("+:", a+b)

print("-:", a-b)

print("*:", a*b)

print("a==b:", a==b)

print("a!=b:", a!=b)

print("a<b:", a<b)

print("a>b:", a>b)

print("a<=b:", a<=b)

print("a>=b:", a>=b)

print("float:", float(a), float(b))

print("int:", int(a), int(b))

print("str:", a.pp(), b.pp())  # pp : pretty print
