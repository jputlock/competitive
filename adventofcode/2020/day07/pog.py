# from ..util.inputs import *
import collections
import functools
import itertools
import operator
import os
import re
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

	regex = r"(\w+? \w+?) bags? contain ((\d+ (\w+? \w+?) bags?(, )?)+|(no other bags))."
	bag_dict = dict()

	for line in data:
		match = re.match(regex, line)
		holder = match.group(1)
		for piece in match.group(2).split(", "):
			print("LINE: " + piece)
			if "no other bags" in piece:
				continue
			num = int(piece.split(" ")[0])
			bag_type = " ".join(piece.split(" ")[1:3])
			if holder not in bag_dict:
				bag_dict[holder] = dict()
			bag_dict[holder][bag_type] = num
	
	holder = "shiny gold"

	ans = dfs(bag_dict, holder) - 1

	yield ans

def dfs(bag_dict, name):
	if name not in bag_dict:
		return 1
	total = 0
	for neighbor in bag_dict[name]:
		print(name + " holds " + str(bag_dict[name][neighbor]) + " " + neighbor)
		total += bag_dict[name][neighbor] * dfs(bag_dict, neighbor)
	return 1 + total

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()