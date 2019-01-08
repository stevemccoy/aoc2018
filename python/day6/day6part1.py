import fileinput
import numpy as np
import re

pattern = re.compile(r'(?P<x>.+), (?P<y>.+)')

class Location:
	def __init__(self, id, x, y):
		self.id = id
		self.x = x
		self.y = y
		self.distance = {}
		self.landmark = None

	def closest_landmarks(self):
		winners = []
		min_distance = 9999
		for (loc,distance) in self.distance.items():
			if distance < min_distance:
				winners = [loc]
			elif distance == min_distance:
				winners.append(loc)
		return winners


def distance(loc1 :Location, loc2 :Location):
	dx = loc1.x - loc2.x
	dy = loc1.y - loc2.y
	return (dx if dx >= 0 else -dx) + (dy if dy >= 0 else -dy)

def read_input():
	d = []
	n = 0
	for line in fileinput.input():
		x, y = pattern.match(line).groups()
		loc = Location(n, int(x), int(y))
		d.append(loc)
		n += 1
	return d

def find_bounds(list):
	lbx = 1000
	lby = 1000
	ubx = 0
	uby = 0
	for loc in list:
		lbx = min(lbx, loc.x)
		lby = min(lby, loc.y)
		ubx = max(ubx, loc.x)
		uby = max(uby, loc.y)
	return lbx - 1, lby - 1, ubx + 1, uby + 1

def create_distance_grid(xfrom, yfrom, xto, yto):
	return [[Location(-1, x, y) for y in range(yfrom, yto + 1, 1)] for x in range(xfrom, xto + 1, 1)]

def update_distance_grid(grid, location):
	for row in grid:
		for cell in row:
			cell.distance[location.id] = distance(cell, location)

def update_all_distances_grid(grid, locations):
	for loc1 in locations:
		update_distance_grid(grid, loc1)

def crown_winning_landmarks(grid):
	for row in grid:
		for cell in row:
			win_list = cell.closest_landmarks()
			if len(win_list) == 1:
				cell.landmark = win_list[0]
			else:
				cell.landmark = -1

def remove_boundary_landmarks(grid, locationObjects):
	kill_list = set([])
	locations = set([loc.id for loc in locationObjects])
	n = len(grid)
	m = len(grid[0])
	for cell in grid[0]:
		if cell.landmark not in kill_list:
			kill_list.add(cell.landmark)
	for cell in grid[n - 1]:
		if cell.landmark not in kill_list:
			kill_list.add(cell.landmark)
	for i in range(n):
		for j in [0, m - 1]:
			cell = grid[i][j]
			if cell.landmark not in kill_list:
				kill_list.add(cell.landmark)
	print('Kill List', kill_list)
	return locations.difference(kill_list)


def count_cells_per_landmark(grid, landmarkSet):
	result = {}
	for locId in landmarkSet:
		result[locId] = 0
	for row in grid:
		for cell in row:
			locId = cell.landmark
			if locId > -1 and locId in result.keys():
				result[locId] += 1
	return result


locations = read_input()
print('Locations:', locations)

xfrom, yfrom, xto, yto = find_bounds(locations)

print('Bounds: ', xfrom, yfrom, xto, yto)

grid = create_distance_grid(xfrom, yfrom, xto, yto)

# Now update the grid with distances for each of the landmarks.
update_all_distances_grid(grid, locations)

# Determine winning landmarks for each cell.
crown_winning_landmarks(grid)

# Eliminate landmarks on the boundary.
location_ids = remove_boundary_landmarks(grid, locations)

# Count winning cells for each landmark.
landmark_counts = count_cells_per_landmark(grid, location_ids)

# Declare a winner.
print(landmark_counts)

