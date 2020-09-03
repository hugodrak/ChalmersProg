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
		import wordfreq
	else:
		spec = importlib.util.spec_from_file_location("wordfreq", src_path+"/wordfreq.py")
		wordfreq = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(wordfreq)

	pass_tests = 0
	fail_tests = 0
	fun_count  = 0

	def printTopMost(freq,n):
		saved = sys.stdout
		sys.stdout = io.StringIO()
		wordfreq.printTopMost(freq,n)
		out = sys.stdout.getvalue()
		sys.stdout = saved
		return out

	if hasattr(wordfreq, "tokenize"):
		fun_count = fun_count + 1
		test(wordfreq.tokenize, [], [])
		test(wordfreq.tokenize, [""], [])
		test(wordfreq.tokenize, ["   "], [])
		test(wordfreq.tokenize, ["This is a simple sentence"], ["this","is","a","simple","sentence"])
		test(wordfreq.tokenize, ["I told you!"], ["i","told","you","!"])
		test(wordfreq.tokenize, ["The 10 little chicks"], ["the","10","little","chicks"])
		test(wordfreq.tokenize, ["15th anniversary"], ["15","th","anniversary"])
		test(wordfreq.tokenize, ["He is in the room, she said."], ["he","is","in","the","room",",","she","said","."])
	else:
		print("tokenize is not implemented yet!")

	if hasattr(wordfreq, "countWords"):
		fun_count = fun_count + 1
		test(wordfreq.countWords, ([],[]), {})
		test(wordfreq.countWords, (["clean","water"],[]), {"clean":1,"water":1})
		test(wordfreq.countWords, (["clean","water","is","drinkable","water"],[]), {"clean":1,"water":2,"is":1,"drinkable":1})
		test(wordfreq.countWords, (["clean","water","is","drinkable","water"],["is"]), {"clean":1,"water":2,"drinkable":1})
	else:
		print("countWords is not implemented yet!")

	if hasattr(wordfreq, "printTopMost"):
		fun_count = fun_count + 1
		test(printTopMost,({},10),"")
		test(printTopMost,({"horror": 5, "happiness": 15},0),"")
		test(printTopMost,({"C": 3, "python": 5, "haskell": 2, "java": 1},3),"python                  5\nC                       3\nhaskell                 2\n")
	else:
		print("printTopMost is not implemented yet!")

	print(str(pass_tests)+" out of "+str(pass_tests+fail_tests)+" passed.")

	return (fun_count == 3 and fail_tests == 0)

if __name__ == "__main__":
	run()
