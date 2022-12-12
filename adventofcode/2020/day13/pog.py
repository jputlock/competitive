# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return line

def crt(n, a):
	total = 0
	N = functools.reduce(lambda a, b: a*b, n)
	for ni, ai in zip(n,a):
		p = N // ni
		total += ai * modinv(p, ni) * p
	return total % N

def xgcd(a, b): # ax + by = d
	if a == 0:
		return (b, 0, 1)
	d, y, x = xgcd(b % a, a)
	k = b // a
	return (d, x - k * y, y)

def modinv(a, n):
	d, x, y = xgcd(a,n)
	if d != 1:
		print("FUCK")
	return x % n

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	data = [parse_line(line.strip()) for line in input_file if line.strip()]
	us = int(data[0])
	bus_times = data[1].split(",")

	n, a = [], []
	
	for i,time in enumerate(bus_times):
		if time != "x":
			a.append(int(time) - i)
			n.append(int(time))
	print(a)
	print(n)

	# if crt(n,a) > 100000000000000:
	yield crt(n,a)

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()