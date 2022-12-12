# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return line

def solve():
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	# data = [0,3,6]
	data = [8,13,1,0,18,9]

	nums = dict()
	prev = 0
	overwrite = None

	for turn in range(30000000):
		if turn < len(data):
			nums[data[turn]] = turn
			prev = data[turn]
			continue
		# turn >= len(data)

		if overwrite is None:
			# hasnt been in our dict
			overwrite = nums[0] if 0 in nums else None
			nums[0] = turn

			prev = 0
		else:
			# has been in our dict
			prev = nums[prev] - overwrite
			overwrite = nums[prev] if prev in nums else None
			nums[prev] = turn
			

		
	
	yield prev


def main() -> None:
	"""Called when the script is run."""
	# with open(f'input.txt', 'r') as input_file:
	for solution in solve():
		print(solution)

if __name__ == '__main__':
	main()