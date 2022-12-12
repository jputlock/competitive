# from ..util.inputs import *
import collections
import functools
import itertools
import operator
import os
import regex
import sys
import typing

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

	p_size = 25
	key = 69316178
	# p_size = 5
	# key = 127

	# for i in range(p_size, len(data)):

	# 	found = False
	# 	for j in range(1, p_size):
	# 		for k in range(1, p_size - j + 1):
	# 			if data[i - j] + data[i - (j + k)] == data[i]:
	# 				found = True
	# 				break
	# 		if found:
	# 			break
		
	# 	if not found:
	# 		yield data[i]
	# 		return

	subseq = []
	csum = 0
	for i, ele in enumerate(data):
		# print("PRE",subseq)
		while csum > key:
			csum -= subseq.pop(0)
			# print("POST",subseq)
		if csum < key:
			subseq.append(ele)
			csum += ele
		# print(subseq)
		if csum == key:
			yield min(subseq) + max(subseq)
		



def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()