import fileinput
from collections import deque
import re


def read_input():
	d = deque()
	for line in fileinput.input():
		for ch in line:
			d.append(ch)
	return d


def reacts(chem1, chem2):
	if chem1.lower() == chem2.lower():
		if chem1.islower() and chem2.isupper():
			return True
		elif chem1.isupper() and chem2.islower():
			return True
	else:
		return False

def process(reactants):
	products = deque()
	count = 0
	site1 = None
	site2 = None

	for ch in reactants:
		if site1 is None:
			site1 = ch
		elif site2 is None:
			site2 = ch
		elif reacts(site1, site2):
			site1 = None
			site2 = None
		else:
			products.append(site1)
			site1,site2 = site2,None

	return products


def render(input):
	changes = 1
	d1 = input
	count = len(d1)
	pass_count = 0
	while changes > 0 and count > 0:
		pass_count += 1
		print("Pass", pass_count)
		print("Input", count, "items")
		d2 = process(d1)
		count = len(d2)
		changes = len(d1) - count
		print("Output", count, "items.", changes, "reactions.")
		d1 = d2.copy()
		print(d1)

	print("Finished.", len(d1), "items remaining.")
	print(d1)


d = read_input()
render(d)
