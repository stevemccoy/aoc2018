import fileinput

total = 0
seen = {total:1}
done = False

lines = []
for s in fileinput.input():
	lines.append(s)

while not done:
	for line in lines:
		v = int(line)
		total += v
		if total in seen:
			done = True
			break
		else:
			seen[total] = 1

print('Done. ', total)

