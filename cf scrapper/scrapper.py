import requests

problemset = []
result = ""

def getProblems():
	global problemset
	problemset = requests.get('https://codeforces.com/api/problemset.problems')
	problemset = problemset.json()
	problemset = problemset['result']['problems']
	

def setProblemName(name):
	index = name[-1]
	contestId = name[0: -1]
	ret = name
	global result
	for problem in problemset:
		if str(problem['contestId']) == contestId and problem['index'] == index:
			ret = ret + " " + problem['name']
	result = result + ret + '\n'
	if ret == "":
		print("problem {} failed".format(name))
	
getProblems()
inp = open("input.txt", "r")
output = open("output.txt", "w")

for problem in inp:
	setProblemName(problem.rstrip().lstrip())
output.write(result)
