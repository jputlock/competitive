# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing
import math

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return line

def rotate(pos, ccw):
	for _ in range(ccw):
		pos = (-pos[1], pos[0])
	return pos

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	data = [parse_line(line.strip()) for line in input_file if line.strip()]

	# left = positive
	# right = negative
	wayX, wayY = 10,1
	x,y = 0,0
	for line in data:
		command = line[0]
		num = int(line[1:])

		if command == "N":
			wayY += num
		elif command == "S":
			wayY -= num
		elif command == "E":
			wayX += num
		elif command =="W":
			wayX -= num
		elif command == "L":
			wayX, wayY = rotate([wayX, wayY], num // 90)
		elif command == "R":
			wayX, wayY = rotate([wayX, wayY], (360 - num) // 90)
		elif command == "F":
			x += num*wayX
			y += num*wayY
		print(f"SHIP: {x},{y}")
		print(f"WAY: {wayX},{wayY}")
	
	yield abs(x) + abs(y)

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()