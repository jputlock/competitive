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
	return line

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	data = [parse_line(line.strip()) for line in input_file if line.strip()]
	ran = set()
	ip = 0
	acc = 0

	yield recurse(data, ip, acc, ran, False)

def recurse(data, ip, acc, ran, swap):

	if ip == len(data):
		return acc

	if ip in ran:
		return

	if ip > len(data):
		return acc
		
	line = data[ip]
	print(ip, line)

	ran.add(ip)
	args = line.split(" ")
	
	if args[0] == "jmp":
		ans = recurse(data,ip+int(args[1]),acc,ran,swap)
		if ans: return ans
		
		if not swap:
			ans = recurse(data,ip+1,acc,ran,True)
			if ans: return ans

	elif args[0] == "nop":
		ans = recurse(data,ip+1,acc,ran,swap)
		if ans: return ans
		
		if not swap:
			ans = recurse(data,ip+int(args[1]),acc,ran,True)
			if ans: return ans
	else:
		return recurse(data,ip+1,acc+int(args[1]),ran,swap)
	
	

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()