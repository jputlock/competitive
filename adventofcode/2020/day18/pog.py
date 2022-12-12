# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return line

class Term:
	def __init__(self,val):
		self.val = val
	def __mul__(self,other):
		return Term(self.val * other.val)
	def __mod__(self,other):
		return Term(self.val + other.val)
	def __sub__(self,other):
		return Term(self.val * other.val)
	def __repr__(self):
		return f'Term({self.val})'

def part1(expr):
	ff = regex.sub(r'(\d+)', r'Term(\1)', expr).replace('+','%').replace('*','-')
	return eval(ff).val

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	data = [line for line in input_file if line]
	yield sum(part1(line) for line in data)
	yield str()

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()