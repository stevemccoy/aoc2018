import fileinput

total = 0.0
for line in fileinput.input():
	v = float(line)
	total += v

print(total)

