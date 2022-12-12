# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing

from math import sqrt

from time import time
from discretelog import discrete_log

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return int(line)

def decrypt(a, b, m):
	sz = 1

	curr = a
	while curr != b:
		curr = (curr * a) % m
		sz += 1
	return sz

def encrypt(a, e, m):
	return pow(a, e, m)

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	door, card = [parse_line(line.strip()) for line in input_file if line.strip()]
	
	mod = 5373535535 

	start = time()
	card_sz = decrypt(7, card, mod)
	ans = encrypt(door, card_sz, mod)
	end = time()

	ttime = end-start
	unittime = ttime / mod
	print(f"Took {ttime:.6f} seconds")
	yield ans

	start = time()
	card_sz = discrete_log(7, card, mod)
	ans = encrypt(door, card_sz, mod)
	end = time()
	 
	ttime2 = end-start
	print(f"Took {ttime2:.6f} seconds")
	# print(f"Scaling to {unittime*sqrt(mod):.6f} seconds")
	yield ans


	

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()