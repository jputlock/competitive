# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return line

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	data = [parse_line(line.strip()) for line in input_file if line.strip()]

	board = collections.defaultdict(bool)

	for line in data:
		pos = (0,0,0)
		i = 0
		while i < len(line):
			direction = line[i]
			if direction == "s" or direction == "n":
				i += 1
				direction += line[i]

			offset = (0,0,0)
			if direction == "w":
				offset = (-1,-1,0)
			elif direction == "e":
				offset = (1,1,0)
			elif direction == "se":
				offset = (1,0,-1)
			elif direction == "sw":
				offset = (0,-1,-1)
			elif direction == "ne":
				offset = (0,1,1)
			elif direction == "nw":
				offset = (-1,0,1)
			
			pos = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2])

			i += 1
		board[pos] = not board[pos]
	
	yield sum(board[x] for x in board)
	
	# board initialized
	
	for day in range(100):
		neighbor_counts = collections.defaultdict(int)

		for pos in board:
			if not board[pos]: # white
				continue
			for offset in [(0,0,0),(-1,-1,0), (1,1,0),(1,0,-1),(0,-1,-1),(0,1,1),(-1,0,1)]:
				tmp = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2])
				neighbor_counts[tmp] += pos != tmp

		for pos, count in neighbor_counts.items():
			if not board[pos] and count == 2:
				board[pos] = True
			elif board[pos] and (count == 0 or count > 2):
				board[pos] = False
		print(sum(board[x] for x in board))

	yield sum(board[x] for x in board)

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()