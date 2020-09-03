import io
import sys
import importlib.util

def testEq(res,ref,msg):
	global pass_tests, fail_tests
	if res == ref:
		pass_tests = pass_tests + 1
	else:
		print(msg)
		print("Got:")
		print(res)
		print("Instead of:")
		print(ref)
		fail_tests = fail_tests + 1

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

	saved_stdout = sys.stdout
	sys.stdout = io.StringIO()
	
	saved_argv = sys.argv
	sys.argv = ["hsum.py","10"]

	if src_path == None:
		import hsum
	else:
		spec = importlib.util.spec_from_file_location("hsum", src_path+"/hsum.py")
		hsum = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(hsum)

	sys.argv = saved_argv

	out = sys.stdout.getvalue()
	sys.stdout = saved_stdout

	pass_tests = 0
	fail_tests = 0
	fun_count  = 0

	if hasattr(hsum, "hSum"):
		fun_count = fun_count + 1
		test(hsum.hSum, 5, 2.283333333333333)
		test(hsum.hSum, 7, 2.5928571428571425)
	else:
		print("hSum is not implemented yet!")

	if hasattr(hsum, "main"):
		fun_count = fun_count + 1
		testEq(out, "0 0\n1 1.0\n2 1.5\n3 1.8333333333333333\n4 2.083333333333333\n5 2.283333333333333\n6 2.4499999999999997\n7 2.5928571428571425\n8 2.7178571428571425\n9 2.8289682539682537\n","function main should generate exactly the same output as in the assignment")
	else:
		print("main is not implemented yet!")

	print(str(pass_tests)+" out of "+str(pass_tests+fail_tests)+" passed.")

	return (fun_count == 2 and fail_tests == 0)

if __name__ == "__main__":
	run()
