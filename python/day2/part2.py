import fileinput

def get_input_lines():
	lines = []
	for line in fileinput.input():
		lines.append(line)
	return lines

def find_matching_pairs(lines):
	pairs = []
	n = len(lines)
	for i in range(n):
		line = lines[i]
		for other in lines[i+1:]:
			if matching_pair(line, other):
				pairs.append((line, other))
	return pairs

def matching_pair(line, other):
	n = len(line)
	diffs = 0
	if len(other) == n:
		for i in range(n):
			if line[i] != other[i]:
				diffs += 1
				if diffs > 1:
					return False
		return diffs == 1
	else:
		return False

def display_matching_pairs(pairs):
	for first,second in pairs:
		print(first, second, common_string(first, second))

def common_string(first, second):
	result = []
	n = len(first)
	for i in range(n):
		if first[i] == second[i]:
			result.append(first[i])
	return ''.join(result)


lines = get_input_lines()
pairs = find_matching_pairs(lines)
display_matching_pairs(pairs)
