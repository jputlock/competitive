# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return list(line)

def num_occupied(i, j, data):
	total = 0
	
	dist = 1
	upL = True
	up = True
	upR = True
	left = True
	right = True
	downL = True
	down = True
	downR = True
	while dist < max(len(data), len(data[0])):
		if up and i - dist >= 0:
			if data[i-dist][j] == "#":
				total += 1
				up = False
			if data[i-dist][j] == "L":
				up = False
		if down and i + dist < len(data):
			if data[i+dist][j] == "#":
				total += 1
				down = False
			if data[i+dist][j] == "L":
				down = False
		if left and j - dist >= 0:
			if data[i][j-dist] == "#":
				total += 1
				left = False
			if data[i][j-dist] == "L":
				left = False
		if right and j + dist < len(data[i]):
			if data[i][j+dist] == "#":
				total += 1
				right = False
			if data[i][j+dist] == "L":
				right = False
		if upL and min(i,j) - dist >= 0:
			if data[i-dist][j-dist] == "#":
				total += 1
				upL = False
			if data[i-dist][j-dist] == "L":
				upL = False
		if upR and i - dist >= 0 and j + dist < len(data[i-dist]):
			if data[i-dist][j+dist] == "#":
				total += 1
				upR = False
			if data[i-dist][j+dist] == "L":
				upR = False
		if downL and i + dist < len(data) and j - dist >= 0:
			if data[i+dist][j-dist] == "#":
				total += 1
				downL = False
			if data[i+dist][j-dist] == "L":
				downL = False
		if downR and i + dist < len(data) and j + dist < len(data[i+dist]):
			if data[i+dist][j+dist] == "#":
				total += 1
				downR = False
			if data[i+dist][j+dist] == "L":
				downR = False
		if not (upL or up or upR or left or right or downL or down or downR):
			break
		dist += 1

	return total
			

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	old_data = [parse_line(line.strip()) for line in input_file if line.strip()]

	occupied = sum(line.count("#") for line in old_data)
	
	changes = 1
	while changes != 0:
		changes = 0
		data = [row[:] for row in old_data]
		# print("\n".join(["".join(x for x in line) for line in data]))
		for i in range(len(data)):
			for j in range(len(data[i])):
				if old_data[i][j] == "L" and num_occupied(i, j, old_data) == 0:
					data[i][j] = "#"
					changes += 1
					occupied += 1
				elif old_data[i][j] == "#" and num_occupied(i,j,old_data) >= 5:
					data[i][j] = "L"
					changes += 1
					occupied -= 1
		old_data = data
		print("\n\n")
	yield occupied

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()