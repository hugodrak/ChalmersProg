import sys

def hSum(n):
	sum = 0
	for val in range(n+1):
		if val > 0:
			sum += 1/val
	return sum


def main():
	for i in range(int(sys.argv[1])):
		print(i, hSum(i))
main()	
