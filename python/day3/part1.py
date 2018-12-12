import fileinput
import copy
import re

pattern = re.compile(r'#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)')

clothsize = 1000
row = [0] * clothsize
cloth = []
for i in range(clothsize):
	cloth.append(copy.deepcopy(row))

for line in fileinput.input():
	elf,x,y,w,h = [int(s) for s in pattern.match(line).groups()]
	for i in range(x, x + w, 1):
		for j in range(y, y + h, 1):
			cloth[i][j] += 1

count = [1 if cell > 1 else 0 for row in cloth for cell in row].count(1)
print(count)

