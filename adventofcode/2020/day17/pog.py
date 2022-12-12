# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return line

def neighborhood(*position):
	for offset in itertools.product([-1, 0, 1], repeat=len(position)):
		yield tuple(pos + offset[i] for i, pos in enumerate(position))
	
def run_simulation(init_grid, num_dims):
	grid = collections.defaultdict(lambda: ".")

	rest = (0,)*(num_dims-2)
	for x, line in enumerate(init_grid):
		for y, state in enumerate(line):
			grid[(x, y) + rest] = state

	for step in range(6):
		neighbor_counts = collections.defaultdict(int)

		for pos in grid:
			if grid[pos] == ".":
				continue
			for neighbor in neighborhood(*pos):
				neighbor_counts[neighbor] += pos != neighbor
		
		for pos, count in neighbor_counts.items():
			if grid[pos] == "#" and count not in [2,3]:
				grid[pos] = "."
			elif grid[pos] == "." and count == 3:
				grid[pos] = "#"
		

	return sum(state == "#" for state in grid.values())
			

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	data = [parse_line(line.strip()) for line in input_file if line.strip()]
	yield run_simulation(data, 3)
	yield run_simulation(data, 4)

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()