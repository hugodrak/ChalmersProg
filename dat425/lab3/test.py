import io
import sys
import importlib.util

def test(fun,x,y):
	global pass_tests, fail_tests
	if type(x) == tuple:
		z = fun(*x)
	else:
		z = fun(x)
	if y == z:
		pass_tests = pass_tests + 1
	else:
		if type(x) == tuple:
			s = repr(x)
		else:
			s = "("+repr(x)+")"
		print("Condition failed:")
		print("   "+fun.__name__+s+" == "+repr(y))
		print(fun.__name__+" returned/printed:")
		print(str(z))
		fail_tests = fail_tests + 1

def run(src_path=None):
	global pass_tests, fail_tests

	if src_path == None:
		import matrix
	else:
		spec = importlib.util.spec_from_file_location("matrix", src_path+"/matrix.py")
		matrix = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(matrix)

	pass_tests = 0
	fail_tests = 0
	fun_count  = 0

	if hasattr(matrix, "loadtxt"):
		fun_count = fun_count + 1
	else:
		print("loadtxt is not implemented yet!")

	if hasattr(matrix, "powers"):
		fun_count = fun_count + 1
		test(matrix.powers, ([],0,10), [])
		test(matrix.powers, ([2],0,2), [[1, 2, 4]])
		test(matrix.powers, ([2],0,0), [[1]])
		test(matrix.powers, ([2],0,-1), [[]])
		test(matrix.powers, ([2,3],0,2), [[1, 2, 4], [1, 3, 9]])
	else:
		print("powers is not implemented yet!")

	if hasattr(matrix, "transpose"):
		fun_count = fun_count + 1
		test(matrix.transpose, [], [])
		test(matrix.transpose, [[1]], [[1]])
		test(matrix.transpose, [[1,2,3]], [[1],[2],[3]])
		test(matrix.transpose, [[1,2,3],[4,5,6]], [[1,4],[2,5],[3,6]])
	else:
		print("transpose is not implemented yet!")

	if hasattr(matrix, "matmul"):
		fun_count = fun_count + 1
		test(matrix.matmul, ([],[]), [])
		test(matrix.matmul, ([[2]],[[4]]), [[8]])
		test(matrix.matmul, ([[2,1]],[[4],[3]]), [[11]])
		test(matrix.matmul, ([[1,2],[3,4]],[[0,1],[1,0]]), [[2, 1], [4, 3]])
		test(matrix.matmul, ([[1,2],[3,4]],[[1,0],[0,1]]), [[1, 2], [3, 4]])
		test(matrix.matmul, ([[1,2],[3,4],[5,6]],[[1,1,1],[1,1,1]]), [[3, 3, 3], [7, 7, 7], [11, 11, 11]])
		test(matrix.matmul, ([[1, 2, 3], [4, 5, 6]],[[7,8,9,10],[11,12,13,14],[15,16,17,18]]), [[74, 80, 86, 92], [173, 188, 203, 218]])
		test(matrix.matmul, ([[1, 2, 3], [4, 5, 6],[7,8,9]], [[1, 0, 0], [0, 1, 0],[0,0,1]]), [[1, 2, 3], [4, 5, 6],[7,8,9]])
		test(matrix.matmul, ([[1, 0, 0], [0, 1, 0],[0,0,1]], [[1, 2, 3], [4, 5, 6],[7,8,9]]), [[1, 2, 3], [4, 5, 6],[7,8,9]])
	else:
		print("matmul is not implemented yet!")

	if hasattr(matrix, "invert"):
		fun_count = fun_count + 1
		test(matrix.invert, [[1,0],[0,1]], [[1,0],[0,1]])
		test(matrix.invert, [[0,1],[1,0]], [[0,1],[1,0]])
		test(matrix.invert, [[1,2],[3,4]], [[-2.0, 1.0], [1.5, -0.5]])
	else:
		print("invert is not implemented yet!")

	print(str(pass_tests)+" out of "+str(pass_tests+fail_tests)+" passed.")

	return (fun_count == 5 and fail_tests == 0)

if __name__ == "__main__":
	run()
