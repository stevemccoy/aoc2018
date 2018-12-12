import fileinput


def frequency_map(line):
	map = dict()
	for c in line:
		if c in map:
			map[c] += 1
		else:
			map[c] = 1
	return map

def has_two_instance(map):
	return 2 in map.values()

def has_three_instance(map):
	return 3 in map.values()


count_pairs = 0
count_triples = 0
for line in fileinput.input():
	map = frequency_map(line)
	if has_two_instance(map):
		count_pairs += 1
	if has_three_instance(map):
		count_triples += 1

checksum = count_pairs * count_triples
print(count_pairs, 'pairs x', count_triples, '=', checksum)
