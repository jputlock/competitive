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
	
	mem = dict()

	orig_mask = ""
	mask = ""
	inds = []
	for line in data:
		if regex.match(r"mask = \w+", line):
			orig_mask = mask = regex.match(r"mask = (\w+)", line).group(1)
			inds = [i for i, val in enumerate(mask) if val == "X"]
		elif regex.match(r"mem\[(\d+)\] = \d+", line):
			addr, val = [int(x) for x in regex.match(r"mem\[(\d+)\] = (\d+)", line).groups()]
			print(addr, val)
			# # part 1
			# val |= int(mask.replace("X", "0"), 2)
			# val &= int(mask.replace("X", "1"), 2)
			# mem[addr] = val

			# part 2
			addresses = set()
			for comb in itertools.product('01', repeat=len(inds)):
				addr |= int(mask.replace("X", "0"), 2)
				
				new_addr = ""
				j = 0
				for i in range(36):
					if i in inds:
						new_addr = new_addr + comb[j]
						j += 1
					else:
						new_addr = new_addr + bin(addr)[2:].zfill(36)[i]
				addresses.add(int(new_addr, 2))


			for address in addresses:
				print(f'mem[{address}] = {val}')
				mem[address] = val

	
	yield sum(mem.values())

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()