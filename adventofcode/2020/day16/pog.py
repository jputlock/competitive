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

	field_dict = dict()
	
	for line in data[:20]:
		match = regex.match(r"(\w+(?: \w+)?): (\d+)-(\d+) or (\d+)-(\d+)", line)
		field = match.group(1)
		a1, a2, b1, b2 = int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5))
		field_dict[field] = (a1, a2, b1, b2)
	
	possibilities = [[field for field in field_dict] for _ in range(len(field_dict))]

	our = [int(x) for x in data[21].split(",")]

	tickets = []

	for line in data[23:]:
		ticket = [int(x) for x in line.split(",")]

		add = True
		for value in ticket:
			valid = False
			for r in field_dict.values():
				if r[0] <= value <= r[1] or r[2] <= value <= r[3]:
					valid = True
					break
			if not valid:
				add = False
				break
		if add:
			tickets.append(ticket)

	# valid tickets only
	for ticket in tickets:
		for i, val in enumerate(ticket):
			j = 0
			while j < len(possibilities[i]):
				field = possibilities[i][j]
				r = field_dict[field]
				if not (r[0] <= val <= r[1] or r[2] <= val <= r[3]):
					possibilities[i].remove(field)
				else:
					j += 1

	len_sort = sorted([(i, x) for i, x in enumerate(possibilities)], key=lambda x: len(x[1]))
	
	fields = [""] * len(len_sort)
	for i in range(len(len_sort)):
		ind = len_sort[i][0]
		field = len_sort[i][1][0]
		for j in range(i, len(len_sort)):
			len_sort[j][1].remove(field)
		fields[ind] = field
	print(fields)

	prod = functools.reduce(lambda a,b: a*b, [our[i] for i, field in enumerate(fields) if field.startswith("departure")])

	yield prod

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()