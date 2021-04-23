f = open("data-mining.md")

res = ""
for line in f:
	line = line.replace("r:**", "r:")
	res = res + line
	
o = open("data-mining.md", "w")
o.write(res)
