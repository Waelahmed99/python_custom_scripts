from random import seed
from random import randint
import os
import shutil
import platform
import subprocess

def generate_cases():

	path = 'tests/'
	seed(1)
	
	try:
		shutil.rmtree(path)
	except:
		pass
	os.mkdir(path)

	cases = int(input("Enter number of test cases: "))
	variables = int(input("Enter number of variables: "))

	if cases <= 0 or variables <= 0:
		print("No tests will be generated, thank you")
		return
	
	print()
	srange = []
	erange = []
	for i in range(variables):
		s = int(input("Enter start range for variable {}: ".format(i+1)))
		srange.append(s)
		e = int(input("Enter end range for variable {}: ".format(i+1)))
		erange.append(e)
	
	print()
	for i in range(cases):
		fileName = path + "test" + str(i + 1)
		f = open(fileName, "x") 
		ans = ""
		for rng in range(variables):
			x = randint(srange[rng], erange[rng])
			ans = ans + " " + str(x)
		f.write(ans.rstrip().lstrip())
		
	print("Done writing {} testcases inside {} folder".format(cases, path))
	
	if platform.system() == "Windows":
		os.startFile(path)
	elif platform.system() == "Drawin":
		subprocess.Popen(["open", path])
	else:
		subprocess.Popen(["xdg-open", path])
		
		
generate_cases()
