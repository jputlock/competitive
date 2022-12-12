# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return int(line)

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	data = [parse_line(line.strip()) for line in input_file if line.strip()]
	
	device = max(data) + 3
	data.append(device)
	nums = sorted(data)

	# part 1
	curr = 0
	diff1, diff3 = 0,0

	for num in nums:
		diff = num - curr
		if diff > 3:
			break
		if diff == 1:
			diff1 += 1
		elif diff == 3:
			diff3 += 1
		curr = num
	
	yield diff1 * diff3

	# part 2

	table = {0:1}
	for num in nums:
		table[num] = sum([table[num-i] for i in range(1,4) if num-i in table])
	yield table[device]

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()